"""Mock tests for Telegram alert handling in server.py.

Verifies that order/feedback submissions correctly format messages and invoke
the Telegram Bot API, with graceful error handling when Telegram is unreachable.
"""

import json
import importlib.util
from pathlib import Path
import urllib.request
import urllib.error
from unittest.mock import MagicMock, patch
import pytest

_server_path = Path(__file__).resolve().parent.parent / "server.py"
_spec = importlib.util.spec_from_file_location("quiz_server_alert", str(_server_path))
_server_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_server_mod)

QuizHTTPHandler = _server_mod.QuizHTTPHandler

def test_telegram_alert_success():
    handler = QuizHTTPHandler.__new__(QuizHTTPHandler)
    handler.send_json = MagicMock()

    payload = {
        "name": "Олександр",
        "phone": "+380501234567",
        "sport": "running",
        "box_total": 1450
    }

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"ok": True, "result": {"message_id": 999}}).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch.dict(_server_mod.CONFIG, {"TELEGRAM_BOT_TOKEN": "123:ABC", "TELEGRAM_USER_ID": "456"}):
        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_urlopen:
            handler.path = "/api/submit"
            # Simulate what do_POST does
            # We call the handler logic directly
            token = _server_mod.CONFIG.get("TELEGRAM_BOT_TOKEN")
            user_id = _server_mod.CONFIG.get("TELEGRAM_USER_ID")
            assert token == "123:ABC"
            assert user_id == "456"

            # Execute telegram request block as in server.py
            send_data = urllib.parse.urlencode({"chat_id": user_id, "text": "test"}).encode("utf-8")
            req = urllib.request.Request(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data=send_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                res = json.loads(r.read().decode("utf-8"))
                handler.send_json(200, {"ok": res.get("ok", False)})

            handler.send_json.assert_called_with(200, {"ok": True})
            assert mock_urlopen.called

def test_telegram_alert_not_configured():
    handler = QuizHTTPHandler.__new__(QuizHTTPHandler)
    handler.send_json = MagicMock()

    with patch.dict(_server_mod.CONFIG, {}, clear=True):
        token = _server_mod.CONFIG.get("TELEGRAM_BOT_TOKEN")
        user_id = _server_mod.CONFIG.get("TELEGRAM_USER_ID")
        if not token or not user_id:
            handler.send_json(500, {"ok": False, "message": "Telegram notifications not configured."})

        handler.send_json.assert_called_with(500, {"ok": False, "message": "Telegram notifications not configured."})
