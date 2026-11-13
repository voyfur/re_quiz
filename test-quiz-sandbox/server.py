"""Local-only HTTP API and static page for the test quiz."""

import argparse
import ipaddress
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from matcher import MatchError, goal_group_options, recommend
from draft_matcher import DraftMatchError, attach_audit_evidence, draft_options, draft_recommend
try:
    from stock_checker import check_stock
except ImportError:
    def check_stock(skus):
        return {}

try:
    from ai_consultant import consult_ai
except ImportError:
    consult_ai = None


ROOT = Path(__file__).resolve().parent
WEB_ROOT = ROOT / "web"
CATALOG_PATH = ROOT / "catalog.json"
PROJECT_ROOT = ROOT.parent
AUDIT_PATH = PROJECT_ROOT / "wiki" / "projects" / "quiz-set-audit.json"
STATIC_FILES = {
    "/": WEB_ROOT / "index.html",
    "/index.html": WEB_ROOT / "index.html",
    "/app.js": WEB_ROOT / "app.js",
    "/styles.css": WEB_ROOT / "styles.css",
    "/draft": WEB_ROOT / "draft.html",
    "/draft.html": WEB_ROOT / "draft.html",
    "/draft.js": WEB_ROOT / "draft.js",
    "/draft.css": WEB_ROOT / "draft.css",
    "/catalog_data.js": WEB_ROOT / "catalog_data.js",
    "/client_matcher.js": WEB_ROOT / "client_matcher.js",
}
MAX_REQUEST_BYTES = 32768


def _load_catalog(path):
    catalog = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(catalog, list) or len(catalog) < 206:
        raise ValueError("Local catalog must contain at least 206 records")
    if len({record.get("set_id") for record in catalog}) != len(catalog):
        raise ValueError("Local catalog set IDs must be unique")
    return catalog


def _short_label(record):
    label = record.get("description") or record.get("title") or ""
    label = " ".join(label.split())
    if len(label) > 100:
        label = label[:97].rsplit(" ", 1)[0] + "…"
    return label


def _options(catalog):
    values = {"goal_options": goal_group_options(catalog)}
    for namespace in ("purpose", "sport", "contains", "item_type", "form", "duration", "race_format"):
        records_by_value = {}
        counts = {}
        for record in catalog:
            for value in record.get("tags", {}).get(namespace, []):
                records_by_value.setdefault(value, record)
                counts[value] = counts.get(value, 0) + 1
        values[namespace + "_options"] = [
            {
                "value": value,
                "label": _short_label(records_by_value[value]) if namespace == "purpose" else value.replace("_", " "),
                "count": counts[value],
            }
            for value in sorted(records_by_value, key=lambda item: item.casefold())
        ]

    prices = [record["price_uah"] for record in catalog]
    sizes = sorted(
        {
            value
            for record in catalog
            for value in record.get("tags", {}).get("shoe_size", [])
        }
    )
    values["shoe_size_options"] = sizes
    values["price_range_uah"] = {"min": min(prices), "max": max(prices)}
    values["catalog_count"] = len(catalog)
    values["price_snapshot_date"] = catalog[0]["price_snapshot_date"]
    values["test_only"] = True
    return values


def make_handler(catalog):
    """Create the request handler used by the server and handler-level tests."""
    options = _options(catalog)
    class QuizHandler(BaseHTTPRequestHandler):
        server_version = "RaceExpertTestQuiz/0.1"

        def _send(self, status, body, content_type):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; connect-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)

        def _send_json(self, status, payload):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self._send(status, body, "application/json; charset=utf-8")

        def do_GET(self):
            parsed = urlsplit(self.path)
            path = parsed.path
            if path == "/api/options":
                self._send_json(200, options)
                return
            if path == "/api/draft/options":
                if not catalog or "matching_evidence" not in catalog[0]:
                    self._send_json(503, {"test_only": True, "error": "Draft evidence is unavailable"})
                    return
                query = parse_qs(parsed.query)
                goal_group = query.get("goal_group", [None])[0]
                answers = {
                    key: values[-1]
                    for key, values in query.items()
                    if key != "goal_group" and values
                }
                try:
                    self._send_json(200, draft_options(catalog, goal_group, answers))
                except DraftMatchError as error:
                    self._send_json(400, {"test_only": True, "error": str(error)})
                return

            file_path = STATIC_FILES.get(path)
            if file_path is None or not file_path.is_file():
                self._send_json(404, {"test_only": True, "error": "Not found", "results": []})
                return

            content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
            body = file_path.read_bytes()
            if content_type.startswith("text/") or content_type in ("application/javascript",):
                content_type += "; charset=utf-8"
            self._send(200, body, content_type)

        def do_POST(self):
            path = urlsplit(self.path).path
            if path not in ("/api/recommend", "/api/draft/recommend", "/api/check-stock"):
                self._send_json(404, {"test_only": True, "error": "Not found", "results": []})
                return

            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                self._send_json(400, {"test_only": True, "error": "Invalid Content-Length", "results": []})
                return
            if length <= 0 or length > MAX_REQUEST_BYTES:
                self._send_json(400, {"test_only": True, "error": "Request body must be 1–32768 bytes", "results": []})
                return
            if "application/json" not in self.headers.get("Content-Type", "").lower():
                self._send_json(415, {"test_only": True, "error": "Content-Type must be application/json", "results": []})
                return

            try:
                request = json.loads(self.rfile.read(length).decode("utf-8"))
                if path == "/api/check-stock":
                    skus = request.get("skus", [])
                    if not isinstance(skus, list):
                        self._send_json(400, {"test_only": True, "error": "skus must be a list"})
                        return
                    stock_data = check_stock(skus)
                    self._send_json(200, {"test_only": True, "stocks": stock_data})
                    return
                elif path == "/api/ai-consult":
                    user_req = request.get("user_request", {})
                    raw_candidates = request.get("candidates", [])
                    locale = request.get("locale", "uk")
                    catalog_by_row = {item.get("catalog_row"): item for item in catalog} if catalog else {}
                    candidates = []
                    for c in raw_candidates:
                        if isinstance(c, dict):
                            full_item = catalog_by_row.get(c.get("catalog_row"))
                            if full_item:
                                enriched = dict(full_item)
                                enriched.update(c)
                                if not enriched.get("composition"):
                                    enriched["composition"] = full_item.get("composition")
                                if not enriched.get("matching_evidence"):
                                    enriched["matching_evidence"] = full_item.get("matching_evidence")
                                candidates.append(enriched)
                                continue
                        candidates.append(c)
                    ai_result = consult_ai(user_req, candidates, locale) if consult_ai else None
                    self._send_json(200, {"test_only": True, "ok": bool(ai_result), "data": ai_result})
                    return
                elif path == "/api/draft/recommend":
                    if not catalog or "matching_evidence" not in catalog[0]:
                        self._send_json(503, {"test_only": True, "error": "Draft evidence is unavailable", "results": []})
                        return
                    response = draft_recommend(catalog, request)
                else:
                    response = recommend(catalog, request)
            except (UnicodeDecodeError, json.JSONDecodeError):
                self._send_json(400, {"test_only": True, "error": "Request body must be valid UTF-8 JSON", "results": []})
                return
            except (MatchError, DraftMatchError) as error:
                self._send_json(400, {"test_only": True, "error": str(error), "results": []})
                return

            self._send_json(200, response)

        def log_message(self, format_string, *args):
            print("[local test quiz] " + format_string % args)

    return QuizHandler


def create_server(host="127.0.0.1", port=8765, catalog_path=CATALOG_PATH, audit_path=None):
    """Create an HTTP server bound only to a loopback IP address."""
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        raise ValueError("host must be a numeric loopback IP address")
    if not address.is_loopback:
        raise ValueError("test quiz server may bind only to a loopback address")

    catalog = _load_catalog(catalog_path)
    if audit_path is not None:
        audit = json.loads(Path(audit_path).read_text(encoding="utf-8"))
        catalog = attach_audit_evidence(catalog, audit)
    class LocalThreadingHTTPServer(ThreadingHTTPServer):
        daemon_threads = True
        allow_reuse_address = True

    return LocalThreadingHTTPServer((str(address), port), make_handler(catalog))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", help="loopback IP only (default: 127.0.0.1)")
    parser.add_argument("--port", default=8765, type=int)
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    args = parser.parse_args()
    audit_path = AUDIT_PATH if args.catalog == CATALOG_PATH else None
    server = create_server(args.host, args.port, args.catalog, audit_path)
    print("Test-only quiz: http://{}:{}/ (206 catalog records)".format(*server.server_address[:2]))
    print("Press Ctrl+C to stop. Answers are not saved.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping local test quiz.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
