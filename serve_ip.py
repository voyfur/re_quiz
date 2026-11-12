#!/usr/bin/env python3
"""HTTP server bound to 0.0.0.0 to serve the external quiz page by IP."""

import argparse
import http.server
import socket
import socketserver
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC_DIR = ROOT / "public"

import json
import sys

SANDBOX_DIR = ROOT / "test-quiz-sandbox"
if str(SANDBOX_DIR) not in sys.path:
    sys.path.insert(0, str(SANDBOX_DIR))

try:
    from stock_checker import check_stock
except ImportError:
    check_stock = None

try:
    from ai_consultant import consult_ai
except ImportError:
    consult_ai = None

def get_local_ips():
    ips = ["127.0.0.1"]
    try:
        # Connect to an external host to determine default routing interface IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if ip not in ips:
            ips.append(ip)
    except Exception:
        pass
    return ips

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "app": "Race Expert Quiz Local"}).encode("utf-8"))
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/check-stock":
            length = int(self.headers.get("Content-Length", 0))
            if length <= 0 or length > 65536:
                self.send_response(400)
                self.end_headers()
                return
            try:
                body = json.loads(self.rfile.read(length).decode("utf-8"))
                skus = body.get("skus", [])
                stock_data = check_stock(skus) if check_stock else {}
                response_bytes = json.dumps({"ok": True, "stocks": stock_data}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(response_bytes)
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
                return
        elif self.path == "/api/ai-consult":
            length = int(self.headers.get("Content-Length", 0))
            if length <= 0 or length > 65536:
                self.send_response(400)
                self.end_headers()
                return
            try:
                body = json.loads(self.rfile.read(length).decode("utf-8"))
                user_req = body.get("user_request", {})
                candidates = body.get("candidates", [])
                locale = body.get("locale", "uk")
                ai_result = consult_ai(user_req, candidates, locale) if consult_ai else None
                response_bytes = json.dumps({"ok": bool(ai_result), "data": ai_result}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(response_bytes)
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
                return
        self.send_response(404)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format_string, *args):
        print(f"[RaceExpert Quiz] {self.address_string()} - {format_string % args}")

def main():
    parser = argparse.ArgumentParser(description="Serve Quiz by IP")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface (default: 0.0.0.0)")
    parser.add_argument("--port", default=8080, type=int, help="Port (default: 8080)")
    args = parser.parse_args()

    class ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True
        allow_reuse_address = True

    server = ThreadedServer((args.host, args.port), QuietHandler)
    local_ips = get_local_ips()
    
    print("=" * 60)
    print("🚀 RACE EXPERT — ВНЕШНЯЯ СТРАНИЦА КВИЗА ЗАПУЩЕНА")
    print("=" * 60)
    print("Доступ по IP-адресам:")
    for ip in local_ips:
        print(f"  👉 http://{ip}:{args.port}/")
    print(f"  👉 http://localhost:{args.port}/")
    print("=" * 60)
    print("Нажмите Ctrl+C для остановки сервера.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
