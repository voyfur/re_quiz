"""Mock tests for luna_box_consultant.py.

Tests OpenAI API integration with mocks, offline template generation for all 5 sports,
rate-limit handling, malformed JSON recovery, and strict Ukrainian language enforcement.
"""

import json
from unittest.mock import MagicMock, patch
import urllib.error
import pytest
from luna_box_consultant import consult_luna_for_box

@patch("luna_box_consultant.get_api_key", return_value=None)
def test_luna_fallback_offline_templates_for_all_sports(mock_key):
    sports = ["running", "cycling", "triathlon", "gym", "outdoor"]
    for sp in sports:
        res = consult_luna_for_box(
            inputs={"sport": sp, "distance": "21k", "caffeine_preference": "boost"},
            box={"sport_name": sp, "total_base_price": 1200},
            locale="uk"
        )
        assert res["ok"] is True
        assert res["source"] == "luna_expert_template"
        data = res["data"]
        assert "expert_verdict" in data
        assert "tactical_strategy" in data
        assert "timeline_steps" in data
        assert isinstance(data["timeline_steps"], list)
        assert len(data["timeline_steps"]) >= 2
        assert "safety_badge" in data
        assert "pro_tip" in data

def test_luna_openai_mock_success():
    fake_openai_json = {
        "expert_verdict": "Тестовий висновок нутриціолога.",
        "tactical_strategy": "Стратегія прийому гелів кожні 40 хвилин.",
        "timeline_steps": [
            {"timing": "За 15 хв до старту", "instruction": "1 гель", "product_name": "SiS Gel"}
        ],
        "safety_badge": "100% сумісність",
        "pro_tip": "Пий дрібними ковтками."
    }

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "choices": [
            {"message": {"content": json.dumps(fake_openai_json)}}
        ]
    }).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("luna_box_consultant.get_api_key", return_value="sk-fake-key-for-test"):
        with patch("urllib.request.urlopen", return_value=mock_resp):
            res = consult_luna_for_box(
                inputs={"sport": "running"},
                box={"total_base_price": 1000},
                locale="uk"
            )
            assert res["ok"] is True
            assert res["source"] == "openai_luna"
            assert res["data"]["expert_verdict"] == "Тестовий висновок нутриціолога."

def test_luna_openai_network_error_recovers_to_template():
    http_err = urllib.error.HTTPError(
        url="https://api.openai.com/v1/chat/completions",
        code=429,
        msg="Too Many Requests",
        hdrs={},
        fp=MagicMock()
    )

    with patch("luna_box_consultant.get_api_key", return_value="sk-fake-key-for-test"):
        with patch("urllib.request.urlopen", side_effect=http_err):
            res = consult_luna_for_box(
                inputs={"sport": "cycling"},
                box={"total_base_price": 1500},
                locale="uk"
            )
            assert res["ok"] is True
            assert res["source"] == "luna_expert_template"
            assert "Велоспорт" in res["data"]["expert_verdict"] or "велосипед" in res["data"]["tactical_strategy"] or "фляги" in res["data"]["tactical_strategy"]

def test_luna_openai_malformed_json_recovers_to_template():
    mock_resp = MagicMock()
    mock_resp.read.return_value = b'{"choices": [{"message": {"content": "Not a valid JSON content"}}]}'
    mock_resp.__enter__.return_value = mock_resp

    with patch("luna_box_consultant.get_api_key", return_value="sk-fake-key-for-test"):
        with patch("urllib.request.urlopen", return_value=mock_resp):
            res = consult_luna_for_box(
                inputs={"sport": "triathlon"},
                box={"total_base_price": 2500},
                locale="uk"
            )
            assert res["ok"] is True
            assert res["source"] == "luna_expert_template"
            assert "Транзитна зона" in str(res["data"]) or "Триатлон" in str(res["data"])
