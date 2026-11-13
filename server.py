#!/usr/bin/env python3
"""Race Expert Quiz Production Server.

Serves the standalone bilingual Race Expert Quiz, live stock checks from OpenCart MySQL,
recommendation API, AI Consultant via GPT Luna, and Telegram submissions.
"""

from __future__ import annotations

import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
SANDBOX_ROOT = ROOT / "test-quiz-sandbox"
if SANDBOX_ROOT.exists():
    sys.path.insert(0, str(SANDBOX_ROOT))

CATALOG_PATH = SANDBOX_ROOT / "catalog.json" if (SANDBOX_ROOT / "catalog.json").exists() else ROOT / "catalog.json"
AUDIT_PATH = SANDBOX_ROOT / "quiz-set-audit.json" if (SANDBOX_ROOT / "quiz-set-audit.json").exists() else ROOT / "quiz-set-audit.json"
INDEX_PATH = ROOT / "public" / "index.html" if (ROOT / "public" / "index.html").exists() else (ROOT / "quiz.html" if (ROOT / "quiz.html").exists() else ROOT / "index.html")

MAX_BODY = 200_000

# Try importing matching and stock modules
try:
    from draft_matcher import attach_audit_evidence, draft_options, draft_recommend, DraftMatchError
except ImportError:
    draft_options = draft_recommend = DraftMatchError = None
    attach_audit_evidence = lambda cat, audit: cat

try:
    from stock_checker import check_stock
except ImportError:
    def check_stock(skus):
        return {}

try:
    from ai_consultant import consult_ai
except ImportError:
    consult_ai = None


def read_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        if not path.is_file():
            return values
    except Exception:
        return values
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            values[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass
    return values


def load_config() -> dict[str, str]:
    config = {}
    for env_file in [
        ROOT / ".env",
        SANDBOX_ROOT / ".env",
        Path("/etc/race-expert-quiz/telegram.env"),
        Path("/etc/race-expert-quiz/mysql.env"),
        Path("/etc/race-expert-quiz/openai.env"),
    ]:
        config.update(read_dotenv(env_file))
    for k, v in os.environ.items():
        config[k] = v
    return config


CONFIG = load_config()

# Pre-load catalog
CATALOG = []
if CATALOG_PATH.exists() and AUDIT_PATH.exists():
    try:
        raw_catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        raw_audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
        CATALOG = attach_audit_evidence(raw_catalog, raw_audit)
        print(f"Loaded {len(CATALOG)} catalog items with audit evidence.")
    except Exception as e:
        print(f"Warning: Failed to load catalog with audit evidence: {e}")
        try:
            CATALOG = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        except Exception:
            CATALOG = []


class QuizHTTPHandler(BaseHTTPRequestHandler):
    server_version = "RaceExpertQuiz/2.0"

    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_HEAD(self) -> None:
        self.do_GET()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        path = self.path.split("?")[0]
        if path in {"", "/", "/index.html", "/quiz.html"}:
            if not INDEX_PATH.is_file():
                self.send_error(404, "index.html not found")
                return
            body = INDEX_PATH.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-cache")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com https://fonts.googleapis.com https://fonts.gstatic.com;"
            )
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/api/health":
            self.send_json(200, {
                "status": "ok",
                "app": "Race Expert Quiz",
                "catalog_count": len(CATALOG),
                "ai_enabled": bool(consult_ai),
                "timestamp": datetime.now(ZoneInfo("Europe/Kyiv")).isoformat(),
            })
            return

        if path == "/api/options":
            if draft_options and CATALOG:
                self.send_json(200, draft_options(CATALOG))
            else:
                self.send_json(200, {"catalog_count": len(CATALOG)})
            return

        # Fallback to local files if any (e.g. catalog_data.js, client_matcher.js, etc.)
        for search_dir in [ROOT / "public", SANDBOX_ROOT / "web", ROOT]:
            local_file = search_dir / path.lstrip("/")
            if local_file.is_file() and not str(local_file).endswith((".env", ".py")):
                content_type = mimetypes.guess_type(str(local_file))[0] or "application/octet-stream"
                body = local_file.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

        self.send_error(404)

    def do_POST(self) -> None:
        path = self.path.split("?")[0]
        if path not in {"/api/check-stock", "/api/draft/recommend", "/api/submit", "/api/ai-consult"}:
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(400, {"error": "Invalid Content-Length"})
            return
        if length <= 0 or length > MAX_BODY:
            self.send_json(413, {"error": "Body empty or too large"})
            return

        try:
            body_bytes = self.rfile.read(length)
            payload = json.loads(body_bytes.decode("utf-8"))
        except Exception:
            self.send_json(400, {"error": "Invalid UTF-8 JSON"})
            return

        if path == "/api/check-stock":
            skus = payload.get("skus", [])
            if not isinstance(skus, list):
                self.send_json(400, {"error": "skus must be a list"})
                return
            stock_data = check_stock(skus)
            self.send_json(200, {"ok": True, "stocks": stock_data})
            return

        if path == "/api/ai-consult":
            user_req = payload.get("user_request", {})
            raw_candidates = payload.get("candidates", [])
            locale = payload.get("locale", "uk")
            catalog_by_row = {item.get("catalog_row"): item for item in CATALOG} if CATALOG else {}
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
            self.send_json(200, {"ok": bool(ai_result), "data": ai_result})
            return

        if path == "/api/draft/recommend":
            if not draft_recommend:
                self.send_json(500, {"error": "Matcher module not available"})
                return
            try:
                res = draft_recommend(CATALOG, payload)
                self.send_json(200, res)
            except DraftMatchError as e:
                self.send_json(400, {"error": str(e)})
            except Exception as e:
                self.send_json(500, {"error": f"Matching error: {e}"})
            return

        if path == "/api/submit":
            token = CONFIG.get("TELEGRAM_BOT_TOKEN") or CONFIG.get("TELEGRA_BOT_TOKEN")
            user_id = CONFIG.get("TELEGRAM_USER_ID")
            if not token or not user_id:
                self.send_json(500, {"ok": False, "message": "Telegram notifications not configured."})
                return
            try:
                msg = f"🛒 Заявка з Race Expert Quiz\nЧас: {datetime.now(ZoneInfo('Europe/Kyiv')).strftime('%Y-%m-%d %H:%M')}\n\nДані:\n{json.dumps(payload, ensure_ascii=False, indent=2)}"
                send_data = urllib.parse.urlencode({
                    "chat_id": user_id,
                    "text": msg[:4000]
                }).encode("utf-8")
                req = urllib.request.Request(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    data=send_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=10) as r:
                    res = json.loads(r.read().decode("utf-8"))
                    self.send_json(200, {"ok": res.get("ok", False)})
            except Exception as e:
                self.send_json(500, {"ok": False, "message": str(e)})
            return


def main():
    host = os.environ.get("BIND_HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), QuizHTTPHandler)
    print(f"Race Expert Quiz Server running on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
