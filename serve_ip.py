#!/usr/bin/env python3
"""HTTP server bound to 0.0.0.0 to serve the external quiz page by IP."""

import argparse
import http.server
import socket
import socketserver
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC_DIR = ROOT / "public"

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
