import socket
import ssl
import struct
import hashlib
import os
import sys

def scramble_native_password(password: str, salt: bytes) -> bytes:
    if not password:
        return b''
    p = password.encode('utf-8')
    stage1 = hashlib.sha1(p).digest()
    stage2 = hashlib.sha1(stage1).digest()
    stage3 = hashlib.sha1(salt[:20] + stage2).digest()
    return bytes(a ^ b for a, b in zip(stage1, stage3))

def read_packet(sock):
    header = b''
    while len(header) < 4:
        chunk = sock.recv(4 - len(header))
        if not chunk:
            raise EOFError("Connection closed while reading packet header")
        header += chunk
    payload_len = header[0] | (header[1] << 8) | (header[2] << 16)
    seq = header[3]
    payload = b''
    while len(payload) < payload_len:
        chunk = sock.recv(payload_len - len(payload))
        if not chunk:
            raise EOFError("Connection closed while reading packet payload")
        payload += chunk
    return seq, payload

def write_packet(sock, payload, seq):
    payload_len = len(payload)
    header = bytes([payload_len & 0xFF, (payload_len >> 8) & 0xFF, (payload_len >> 16) & 0xFF, seq & 0xFF])
    sock.sendall(header + payload)

def parse_lenenc_int(data, offset):
    if offset >= len(data):
        return None, offset
    b = data[offset]
    if b < 251:
        return b, offset + 1
    elif b == 251:
        return None, offset + 1 # NULL
    elif b == 252:
        return struct.unpack('<H', data[offset+1:offset+3])[0], offset + 3
    elif b == 253:
        return data[offset+1] | (data[offset+2] << 8) | (data[offset+3] << 16), offset + 4
    elif b == 254:
        return struct.unpack('<Q', data[offset+1:offset+9])[0], offset + 9
    return None, offset + 1

def parse_lenenc_str(data, offset):
    length, offset = parse_lenenc_int(data, offset)
    if length is None:
        return None, offset
    val = data[offset:offset+length].decode('utf-8', errors='replace')
    return val, offset + length

def query(sock, sql: str):
    write_packet(sock, b'\x03' + sql.encode('utf-8'), seq=0)
    seq, resp = read_packet(sock)
    if not resp:
        return []
    if resp[0] == 0xFF:
        err_code = struct.unpack('<H', resp[1:3])[0]
        msg = resp[9:].decode('utf-8', errors='replace') if len(resp) > 9 else resp[3:].decode('utf-8', errors='replace')
        raise RuntimeError(f"MySQL Error {err_code}: {msg}")
    elif resp[0] == 0x00:
        # OK Packet
        return []
    
    col_count, _ = parse_lenenc_int(resp, 0)
    columns = []
    for _ in range(col_count):
        _, col_pkt = read_packet(sock)
        # Parse column definition: catalog, schema, table, org_table, name, org_name
        off = 0
        _, off = parse_lenenc_str(col_pkt, off) # catalog
        _, off = parse_lenenc_str(col_pkt, off) # schema
        _, off = parse_lenenc_str(col_pkt, off) # table
        _, off = parse_lenenc_str(col_pkt, off) # org_table
        name, off = parse_lenenc_str(col_pkt, off) # name
        columns.append(name)
    
    # Read EOF or OK packet following column definitions
    _, eof_or_ok = read_packet(sock)
    
    # Read rows
    rows = []
    while True:
        _, row_pkt = read_packet(sock)
        if not row_pkt:
            break
        if row_pkt[0] == 0xFE and len(row_pkt) < 9:
            # EOF Packet
            break
        elif row_pkt[0] == 0xFF:
            raise RuntimeError("Error packet during row fetching")
        
        row = []
        off = 0
        for _ in range(col_count):
            val, off = parse_lenenc_str(row_pkt, off)
            row.append(val)
        rows.append(dict(zip(columns, row)))
    return rows

def connect(host, port, user, password, db):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10.0)
    s.connect((host, port))
    
    # Read initial handshake
    seq, payload = read_packet(s)
    if payload[0] == 0xFF:
        err_code = struct.unpack('<H', payload[1:3])[0]
        raise RuntimeError(f"Server error on handshake: {payload[3:].decode('utf-8', 'ignore')}")
    
    # Parse server version and salt
    idx = payload.find(b'\x00', 1)
    server_ver = payload[1:idx].decode('latin1')
    idx += 1
    conn_id = struct.unpack('<I', payload[idx:idx+4])[0]
    idx += 4
    salt_part1 = payload[idx:idx+8]
    idx += 8 + 1 # skip 1 byte filler
    cap_lower = struct.unpack('<H', payload[idx:idx+2])[0]
    idx += 2
    charset = payload[idx]
    idx += 1
    status_flags = struct.unpack('<H', payload[idx:idx+2])[0]
    idx += 2
    cap_upper = struct.unpack('<H', payload[idx:idx+2])[0]
    idx += 2
    server_caps = cap_lower | (cap_upper << 16)
    
    auth_data_len = payload[idx]
    idx += 1 + 10 # skip auth_data_len and 10 reserved bytes
    salt_part2_len = max(13, auth_data_len - 8) if auth_data_len > 0 else 12
    salt_part2 = payload[idx:idx+salt_part2_len].rstrip(b'\x00')
    salt = salt_part1 + salt_part2[:12]
    
    # SSL Request Packet
    # CLIENT_LONG_PASSWORD(1), CLIENT_FOUND_ROWS(2), CLIENT_LONG_FLAG(4), CLIENT_CONNECT_WITH_DB(8),
    # CLIENT_PROTOCOL_41(0x200), CLIENT_SSL(0x800), CLIENT_SECURE_CONNECTION(0x8000), CLIENT_PLUGIN_AUTH(0x80000)
    client_flags = 1 | 2 | 4 | 8 | 0x200 | 0x800 | 0x8000 | 0x80000
    ssl_req = struct.pack('<I', client_flags) + struct.pack('<I', 16777215) + bytes([45]) + (b'\x00' * 23)
    write_packet(s, ssl_req, seq=1)
    
    # Wrap in TLS
    tls_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_ctx.check_hostname = False
    tls_ctx.verify_mode = ssl.CERT_NONE
    ssl_sock = tls_ctx.wrap_socket(s, server_hostname=None)
    
    cipher = ssl_sock.cipher()
    tls_version = ssl_sock.version()
    
    # Handshake Response 41
    scramble = scramble_native_password(password, salt)
    resp_payload = struct.pack('<I', client_flags) + struct.pack('<I', 16777215) + bytes([45]) + (b'\x00' * 23)
    resp_payload += user.encode('utf-8') + b'\x00'
    resp_payload += bytes([len(scramble)]) + scramble
    resp_payload += db.encode('utf-8') + b'\x00'
    resp_payload += b'mysql_native_password\x00'
    
    write_packet(ssl_sock, resp_payload, seq=2)
    
    seq, auth_resp = read_packet(ssl_sock)
    if auth_resp[0] == 0xFF:
        err_code = struct.unpack('<H', auth_resp[1:3])[0]
        msg = auth_resp[9:].decode('utf-8', errors='replace') if len(auth_resp) > 9 else auth_resp[3:].decode('utf-8', errors='replace')
        raise RuntimeError(f"Authentication failed (code {err_code}): {msg}")
    elif auth_resp[0] == 0x00:
        pass
    else:
        raise RuntimeError(f"Unexpected auth response byte: {auth_resp[0]:#x}")
        
    return ssl_sock, server_ver, tls_version, cipher

def main():
    host = os.environ.get('MYSQL_HOST')
    port = int(os.environ.get('MYSQL_PORT', '3306'))
    user = os.environ.get('MYSQL_USER')
    password = os.environ.get('MYSQL_PASSWORD')
    db = os.environ.get('MYSQL_DATABASE')
    
    if not all([host, user, password, db]):
        print("Missing required environment variables", file=sys.stderr)
        sys.exit(1)
        
    print(f"Connecting to MySQL {host}:{port} db={db} user={user}...")
    sock, server_ver, tls_ver, cipher = connect(host, port, user, password, db)
    print(f"SUCCESS: Connected to MySQL server {server_ver}")
    print(f"TLS negotiated: {tls_ver}, cipher: {cipher}")
    
    # 1. SELECT DATABASE(), SELECT 1
    res_db = query(sock, "SELECT DATABASE() AS current_db")
    print("SELECT DATABASE():", res_db)
    
    res_1 = query(sock, "SELECT 1 AS test_val")
    print("SELECT 1:", res_1)
    
    # 2. SHOW GRANTS
    grants = query(sock, "SHOW GRANTS FOR CURRENT_USER")
    print(f"SHOW GRANTS ({len(grants)} rows):")
    for g in grants:
        print(" ", list(g.values())[0])
        
    # 3. SHOW COLUMNS and LIMIT 0 for 5 product tables
    tables = [
        "oc_product",
        "oc_product_description",
        "oc_product_attribute",
        "oc_attribute_description",
        "oc_stock_status"
    ]
    
    for t in tables:
        cols = query(sock, f"SHOW COLUMNS FROM {t}")
        col_names = [c.get('Field') for c in cols]
        chk = query(sock, f"SELECT * FROM {t} LIMIT 0")
        print(f"Table {t}: {len(cols)} columns confirmed (LIMIT 0 fetched {len(chk)} rows). Sample cols: {col_names[:5]}")
        
    # 4. Test product lookup on kit SKU RE89450
    test_sku = "RE89450"
    res_prod = query(sock, f"SELECT product_id, model, sku, price, quantity, stock_status_id, status FROM oc_product WHERE model = '{test_sku}' OR sku = '{test_sku}' LIMIT 2")
    print(f"Test lookup for SKU '{test_sku}':", res_prod)

if __name__ == '__main__':
    main()
