"""Stock and availability checker for Race Expert quiz product sets.

Connects to OpenCart MySQL (directly on VPS-61125 or via SSH tunnel in dev),
verifying live quantity, status, and price for product SKUs.
"""

import os
import sys
import socket
import ssl
import struct
import hashlib
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Root paths
SANDBOX_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = SANDBOX_ROOT.parent
DOTENV_PATH = PROJECT_ROOT / ".env"


def _load_env_file(path: Path) -> Dict[str, str]:
    env = {}
    if not path.is_file():
        return env
    try:
        content = path.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass
    return env


def scramble_native_password(password: str, salt: bytes) -> bytes:
    if not password:
        return b""
    p = password.encode("utf-8")
    stage1 = hashlib.sha1(p).digest()
    stage2 = hashlib.sha1(stage1).digest()
    stage3 = hashlib.sha1(salt[:20] + stage2).digest()
    return bytes(a ^ b for a, b in zip(stage1, stage3))


def _read_packet(sock) -> Tuple[int, bytes]:
    header = b""
    while len(header) < 4:
        chunk = sock.recv(4 - len(header))
        if not chunk:
            raise EOFError("Connection closed while reading packet header")
        header += chunk
    payload_len = header[0] | (header[1] << 8) | (header[2] << 16)
    seq = header[3]
    payload = b""
    while len(payload) < payload_len:
        chunk = sock.recv(payload_len - len(payload))
        if not chunk:
            raise EOFError("Connection closed while reading packet payload")
        payload += chunk
    return seq, payload


def _write_packet(sock, payload: bytes, seq: int):
    payload_len = len(payload)
    header = bytes([payload_len & 0xFF, (payload_len >> 8) & 0xFF, (payload_len >> 16) & 0xFF, seq & 0xFF])
    sock.sendall(header + payload)


def _parse_lenenc_int(data: bytes, offset: int) -> Tuple[Optional[int], int]:
    if offset >= len(data):
        return None, offset
    b = data[offset]
    if b < 251:
        return b, offset + 1
    elif b == 251:
        return None, offset + 1  # NULL
    elif b == 252:
        return struct.unpack("<H", data[offset+1:offset+3])[0], offset + 3
    elif b == 253:
        return data[offset+1] | (data[offset+2] << 8) | (data[offset+3] << 16), offset + 4
    elif b == 254:
        return struct.unpack("<Q", data[offset+1:offset+9])[0], offset + 9
    return None, offset + 1


def _parse_lenenc_str(data: bytes, offset: int) -> Tuple[Optional[str], int]:
    length, offset = _parse_lenenc_int(data, offset)
    if length is None:
        return None, offset
    val = data[offset:offset+length].decode("utf-8", errors="replace")
    return val, offset + length


def _mysql_query(sock, sql: str) -> List[Dict[str, Optional[str]]]:
    _write_packet(sock, b"\x03" + sql.encode("utf-8"), seq=0)
    seq, resp = _read_packet(sock)
    if not resp:
        return []
    if resp[0] == 0xFF:
        err_code = struct.unpack("<H", resp[1:3])[0]
        msg = resp[9:].decode("utf-8", errors="replace") if len(resp) > 9 else resp[3:].decode("utf-8", errors="replace")
        raise RuntimeError(f"MySQL Error {err_code}: {msg}")
    elif resp[0] == 0x00:
        return []
    
    col_count, _ = _parse_lenenc_int(resp, 0)
    if col_count is None:
        return []
        
    columns = []
    for _ in range(col_count):
        _, col_pkt = _read_packet(sock)
        off = 0
        _, off = _parse_lenenc_str(col_pkt, off)
        _, off = _parse_lenenc_str(col_pkt, off)
        _, off = _parse_lenenc_str(col_pkt, off)
        _, off = _parse_lenenc_str(col_pkt, off)
        name, off = _parse_lenenc_str(col_pkt, off)
        columns.append(name or f"col_{len(columns)}")
    
    _read_packet(sock)  # EOF / OK after columns
    
    rows = []
    while True:
        _, row_pkt = _read_packet(sock)
        if not row_pkt:
            break
        if row_pkt[0] == 0xFE and len(row_pkt) < 9:
            break
        elif row_pkt[0] == 0xFF:
            raise RuntimeError("Error packet during row fetching")
        
        row = []
        off = 0
        for _ in range(col_count):
            val, off = _parse_lenenc_str(row_pkt, off)
            row.append(val)
        rows.append(dict(zip(columns, row)))
    return rows


def _raw_connect(host: str, port: int, user: str, password: str, db: str, timeout: float = 6.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((host, port))
    
    seq, payload = _read_packet(s)
    if payload[0] == 0xFF:
        raise RuntimeError(f"Server error on handshake: {payload[3:].decode('utf-8', 'ignore')}")
    
    idx = payload.find(b"\x00", 1)
    server_ver = payload[1:idx].decode("latin1")
    idx += 1
    idx += 4  # connection id
    salt_part1 = payload[idx:idx+8]
    idx += 8 + 1  # filler
    cap_lower = struct.unpack("<H", payload[idx:idx+2])[0]
    idx += 2
    idx += 1  # charset
    idx += 2  # status flags
    cap_upper = struct.unpack("<H", payload[idx:idx+2])[0]
    idx += 2
    auth_data_len = payload[idx]
    idx += 1 + 10
    salt_part2_len = max(13, auth_data_len - 8) if auth_data_len > 0 else 12
    salt_part2 = payload[idx:idx+salt_part2_len].rstrip(b"\x00")
    salt = salt_part1 + salt_part2[:12]
    
    client_flags = 1 | 2 | 4 | 8 | 0x200 | 0x800 | 0x8000 | 0x80000
    ssl_req = struct.pack("<I", client_flags) + struct.pack("<I", 16777215) + bytes([45]) + (b"\x00" * 23)
    _write_packet(s, ssl_req, seq=1)
    
    tls_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_ctx.check_hostname = False
    tls_ctx.verify_mode = ssl.CERT_NONE
    ssl_sock = tls_ctx.wrap_socket(s, server_hostname=None)
    
    scramble = scramble_native_password(password, salt)
    resp_payload = struct.pack("<I", client_flags) + struct.pack("<I", 16777215) + bytes([45]) + (b"\x00" * 23)
    resp_payload += user.encode("utf-8") + b"\x00"
    resp_payload += bytes([len(scramble)]) + scramble
    resp_payload += db.encode("utf-8") + b"\x00"
    resp_payload += b"mysql_native_password\x00"
    _write_packet(ssl_sock, resp_payload, seq=2)
    
    seq, auth_resp = _read_packet(ssl_sock)
    if auth_resp[0] == 0xFF:
        err_code = struct.unpack("<H", auth_resp[1:3])[0]
        msg = auth_resp[9:].decode("utf-8", errors="replace") if len(auth_resp) > 9 else auth_resp[3:].decode("utf-8", errors="replace")
        raise RuntimeError(f"Authentication failed ({err_code}): {msg}")
    elif auth_resp[0] != 0x00:
        raise RuntimeError(f"Unexpected auth byte: {auth_resp[0]:#x}")
        
    return ssl_sock


class StockChecker:
    """Manages inventory verification against OpenCart oc_product."""

    def __init__(self, env: Optional[Dict[str, str]] = None):
        self._file_env = _load_env_file(DOTENV_PATH)
        self._env = env or {**self._file_env, **os.environ}
        self._tunnel_proc: Optional[subprocess.Popen] = None
        self._tunnel_port = 3307

    def _ensure_connection(self):
        host = self._env.get("MYSQL_HOST", "173.242.63.36")
        port = int(self._env.get("MYSQL_PORT", "3306"))
        user = self._env.get("MYSQL_USER", "")
        password = self._env.get("MYSQL_PASSWORD", "")
        db = self._env.get("MYSQL_DATABASE", "raceexpertcomua")

        if not user or not password:
            raise RuntimeError("MySQL credentials not configured in environment")

        # 1. Try direct connection first (works if running directly on VPS-61125)
        try:
            return _raw_connect(host, port, user, password, db, timeout=2.0)
        except Exception as direct_err:
            # If direct failed, check if we have SSH credentials to tunnel via VPS-61125
            ssh_host = self._env.get("HOST")
            ssh_key = self._env.get("SSH_PRIVATE_KEY_PATH")
            ssh_user = self._env.get("LOGIN", "root")
            ssh_port = self._env.get("SSH_PORT", "22")

            if not (ssh_host and ssh_key and Path(ssh_key).is_file()):
                raise direct_err

            # Start or reuse SSH tunnel
            if self._tunnel_proc is None or self._tunnel_proc.poll() is not None:
                cmd = [
                    "ssh",
                    "-i", ssh_key,
                    "-p", str(ssh_port),
                    "-o", "StrictHostKeyChecking=no",
                    "-o", "ExitOnForwardFailure=yes",
                    "-L", f"{self._tunnel_port}:{host}:{port}",
                    "-N",
                    f"{ssh_user}@{ssh_host}"
                ]
                self._tunnel_proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(1.2)

            return _raw_connect("127.0.0.1", self._tunnel_port, user, password, db, timeout=4.0)

    def close(self):
        if self._tunnel_proc:
            try:
                self._tunnel_proc.terminate()
                self._tunnel_proc.wait(timeout=1.0)
            except Exception:
                pass
            self._tunnel_proc = None

    def __del__(self):
        self.close()

    def check_stock_for_skus(self, skus: List[str]) -> Dict[str, Dict[str, Any]]:
        """Verify stock availability for a list of SKUs.

        Returns a dictionary mapping each SKU to its stock status:
        {
            "RE89450": {
                "sku": "RE89450",
                "product_id": 7149,
                "in_stock": True,
                "quantity": 15,
                "status": 1,
                "live_price_uah": 1525.0,
                "stock_status_id": 5,
                "stock_status_text_uk": "В наявності",
                "stock_status_text_ru": "В наличии",
                "is_live_check": True
            }
        }
        """
        clean_skus = [s.strip() for s in skus if s and s.strip()]
        if not clean_skus:
            return {}

        sock = None
        try:
            sock = self._ensure_connection()
            safe_skus = [s.replace("'", "") for s in clean_skus]
            sku_list_str = ",".join(f"'{s}'" for s in safe_skus)
            sql = f"""
            SELECT product_id, model, sku, price, quantity, stock_status_id, subtract, status
            FROM oc_product
            WHERE model IN ({sku_list_str}) OR sku IN ({sku_list_str})
            """
            rows = _mysql_query(sock, sql)
            
            results: Dict[str, Dict[str, Any]] = {}
            for r in rows:
                model = r.get("model") or ""
                sku = r.get("sku") or ""
                prod_id = int(r["product_id"]) if r.get("product_id") else None
                quantity = int(r.get("quantity") or 0)
                status = int(r.get("status") or 0)
                stock_status_id = int(r.get("stock_status_id") or 0)
                price = float(r.get("price") or 0.0)

                # OpenCart rule: in_stock if product is enabled (status==1) and physical quantity > 0
                is_in_stock = (status == 1 and quantity > 0)

                info = {
                    "product_id": prod_id,
                    "in_stock": is_in_stock,
                    "quantity": quantity,
                    "status": status,
                    "live_price_uah": round(price, 2),
                    "stock_status_id": stock_status_id,
                    "stock_status_text_uk": "В наявності" if is_in_stock else "Немає в наявності",
                    "stock_status_text_ru": "В наличии" if is_in_stock else "Нет в наличии",
                    "is_live_check": True,
                }
                if model:
                    results[model] = {**info, "sku": model}
                if sku:
                    results[sku] = {**info, "sku": sku}

            # For any requested SKU not found in DB, mark as unknown/unavailable
            for requested in clean_skus:
                if requested not in results:
                    results[requested] = {
                        "sku": requested,
                        "product_id": None,
                        "in_stock": False,
                        "quantity": 0,
                        "status": 0,
                        "live_price_uah": None,
                        "stock_status_id": None,
                        "stock_status_text_uk": "Товар не знайдено",
                        "stock_status_text_ru": "Товар не найден",
                        "is_live_check": True,
                    }
            return results

        except Exception as err:
            # Fallback when DB is unreachable: return optimistic snapshot fallback
            sys.stderr.write(f"[StockChecker] DB verification unavailable: {err}\n")
            fallback: Dict[str, Dict[str, Any]] = {}
            for s in clean_skus:
                fallback[s] = {
                    "sku": s,
                    "product_id": None,
                    "in_stock": True,  # Fallback gracefully so quiz never crashes
                    "quantity": None,
                    "status": 1,
                    "live_price_uah": None,
                    "stock_status_id": None,
                    "stock_status_text_uk": "В наявності (каталог)",
                    "stock_status_text_ru": "В наличии (каталог)",
                    "is_live_check": False,
                }
            return fallback

        finally:
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass


# Singleton accessor
_CHECKER_INSTANCE: Optional[StockChecker] = None

def get_stock_checker() -> StockChecker:
    global _CHECKER_INSTANCE
    if _CHECKER_INSTANCE is None:
        _CHECKER_INSTANCE = StockChecker()
    return _CHECKER_INSTANCE


def check_stock(skus: List[str]) -> Dict[str, Dict[str, Any]]:
    return get_stock_checker().check_stock_for_skus(skus)
