#!/usr/bin/env python3
"""Local questionnaire server; Telegram credentials remain server-side."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
MAX_BODY = 200_000
CORE_QUESTION_IDS = [f"Q-{i:02d}" for i in range(1, 10)]
SET_QUESTION_IDS = ["SET-01", "SET-02"]
OPTIONAL_MODULES = {
    "individual_products": ["PRODUCT-01", "PRODUCT-02"],
    "categories": ["CATEGORY-01"],
    "new_sets": ["NEWSET-01", "NEWSET-02"],
}
QUESTION_MODES = {"ready_sets_only", "ready_sets_and_more"}
OPTIONAL_FORMAT_LABELS = {
    "individual_products": "Окремі товари",
    "categories": "Сторінки категорій або груп товарів",
    "new_sets": "Нові набори з товарів",
}


def read_dotenv() -> dict[str, str]:
    values: dict[str, str] = {}
    path = ROOT / ".env"
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key.strip()] = value
    return values


def config_value(*names: str) -> str:
    env_file = read_dotenv()
    for name in names:
        value = os.environ.get(name) or env_file.get(name)
        if value:
            return value
    return ""


def active_question_ids(answers: dict) -> list[str] | None:
    mode = answers.get("Q-01")
    if mode not in QUESTION_MODES:
        return None

    selected_modules: list[str] = []
    if mode == "ready_sets_and_more":
        raw_modules = answers.get("Q-01-EXTRA")
        if not isinstance(raw_modules, str):
            return None
        selected_modules = raw_modules.split(",")
        if (
            not selected_modules
            or len(selected_modules) != len(set(selected_modules))
            or any(module not in OPTIONAL_MODULES for module in selected_modules)
        ):
            return None
    elif "Q-01-EXTRA" in answers:
        return None

    ids = [CORE_QUESTION_IDS[0]]
    if selected_modules:
        ids.append("Q-01-EXTRA")
    ids.extend(CORE_QUESTION_IDS[1:])
    ids.extend(SET_QUESTION_IDS)
    for module, module_ids in OPTIONAL_MODULES.items():
        if module in selected_modules:
            ids.extend(module_ids)
    return ids


def build_document(payload: dict) -> bytes:
    labels = payload["labels"]
    answers = payload["answers"]
    question_ids = active_question_ids(answers) or []
    stamp = datetime.now(ZoneInfo("Europe/Kyiv")).strftime("%Y-%m-%d %H:%M:%S %Z")
    lines = [
        "ВІДПОВІДІ НА АНКЕТУ ПРО ЛОГІКУ КВІЗУ",
        f"Дата заповнення: {stamp}",
    ]
    for index, question_id in enumerate(question_ids, start=1):
        label = labels[question_id].strip().rstrip("*").strip()
        answer = answers[question_id].strip()
        if question_id == "Q-01":
            answer = {
                "ready_sets_only": "Так, лише готові набори",
                "ready_sets_and_more": "Готові набори та інші формати",
            }.get(answer, answer)
        elif question_id == "Q-01-EXTRA":
            answer = ", ".join(
                OPTIONAL_FORMAT_LABELS.get(value, value)
                for value in answer.split(",")
            )
        lines.extend(["", f"Питання {index}. {label}", answer])
    return "\n".join(lines).encode("utf-8")

def send_document(token: str, chat_id: str, document: bytes) -> None:
    boundary = "----QuizFormBoundary7MA4YWxkTrZu0gW"
    filename = "vidpovidi-" + datetime.now(ZoneInfo("Europe/Kyiv")).strftime("%Y%m%d-%H%M%S") + ".txt"
    caption = "Відповіді на питання про підбір товарів"

    def field(name: str, value: str) -> bytes:
        return (
            "--" + boundary + "\r\n"
            + 'Content-Disposition: form-data; name="' + name + '"\r\n\r\n'
            + value + "\r\n"
        ).encode("utf-8")

    parts = [
        field("chat_id", chat_id),
        field("caption", caption),
        (
            "--" + boundary + "\r\n"
            + 'Content-Disposition: form-data; name="document"; filename="' + filename + '"\r\n'
            + "Content-Type: text/plain; charset=utf-8\r\n\r\n"
        ).encode("utf-8"),
        document,
        ("\r\n--" + boundary + "--\r\n").encode("ascii"),
    ]
    request = urllib.request.Request(
        "https://api.telegram.org/bot" + token + "/sendDocument",
        data=b"".join(parts),
        headers={"Content-Type": "multipart/form-data; boundary=" + boundary},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            detail = json.loads(exc.read().decode("utf-8")).get("description", "Telegram API відхилив надсилання.")
        except Exception:
            detail = "Telegram API відхилив надсилання."
        raise RuntimeError(detail) from None
    except urllib.error.URLError:
        raise RuntimeError("Не вдалося підключитися до Telegram. Перевірте мережу та налаштування сервера.") from None
    if not result.get("ok"):
        raise RuntimeError(result.get("description", "Telegram API відхилив надсилання."))


def validate_payload(payload: object) -> str | None:
    if not isinstance(payload, dict):
        return "Неправильний формат відповідей."
    labels = payload.get("labels")
    answers = payload.get("answers")
    if not isinstance(labels, dict) or not isinstance(answers, dict):
        return "У формі бракує відповідей."
    question_ids = active_question_ids(answers)
    if question_ids is None:
        return "Перевірте вибраний формат результату квізу."
    expected_ids = set(question_ids)
    if set(answers) != expected_ids or set(labels) != expected_ids:
        return "У формі бракує відповідей або є невідомі поля."
    for question_id in question_ids:
        answer = answers.get(question_id)
        label = labels.get(question_id)
        if not isinstance(answer, str) or not answer.strip():
            return "Заповніть усі питання."
        if not isinstance(label, str) or not label.strip():
            return "Не вдалося визначити питання форми."
    return None


class Handler(BaseHTTPRequestHandler):
    server_version = "QuizLocal/1.0"

    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path not in {"/", "/index.html"}:
            self.send_error(404)
            return
        body = (ROOT / "index.html").read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/api/submit":
            self.send_error(404)
            return
        if self.headers.get_content_type() != "application/json":
            self.send_json(415, {"ok": False, "message": "Очікувався запит із відповідями форми."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(400, {"ok": False, "message": "Неправильний розмір запиту."})
            return
        if length <= 0 or length > MAX_BODY:
            self.send_json(413, {"ok": False, "message": "Відповіді порожні або завеликі."})
            return
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.send_json(400, {"ok": False, "message": "Не вдалося прочитати відповіді."})
            return
        error = validate_payload(payload)
        if error:
            self.send_json(400, {"ok": False, "message": error})
            return

        token = config_value("TELEGRAM_BOT_TOKEN", "TELEGRA_BOT_TOKEN")
        chat_id = config_value("TELEGRAM_CHAT_ID", "TELEGRAM_USER_ID")
        if not token or not chat_id:
            self.send_json(503, {"ok": False, "message": "Telegram не налаштований. Перевірте секрети на сервері."})
            return
        try:
            document = build_document(payload)
            send_document(token, chat_id, document)
        except RuntimeError as exc:
            self.send_json(502, {"ok": False, "message": str(exc)})
            return
        self.send_json(200, {"ok": True})

    def log_message(self, format: str, *args) -> None:
        # The default log includes only request metadata, not answer content or credentials.
        super().log_message(format, *args)


def main() -> None:
    raw_port = config_value("PORT") or "8000"
    try:
        port = int(raw_port)
    except ValueError:
        raise SystemExit("PORT має бути числом.")
    if not 1 <= port <= 65535:
        raise SystemExit("PORT поза допустимим діапазоном.")
    bind_host = config_value("BIND_HOST") or "127.0.0.1"
    server = ThreadingHTTPServer((bind_host, port), Handler)
    print("Анкета доступна на " + bind_host + ":" + str(port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

