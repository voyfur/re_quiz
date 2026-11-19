from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_env_example_contains_all_variables():
    env_path = ROOT / ".env.example"
    assert env_path.exists(), ".env.example must exist"
    content = env_path.read_text(encoding="utf-8")
    
    required_keys = [
        "PORT", "BIND_HOST", "BASE_URL",
        "OPENCART_CART_ENDPOINT", "OPENCART_BULK_ENDPOINT", "OPENCART_VIEW_CART_URL",
        "MYSQL_HOST", "MYSQL_PORT", "MYSQL_DATABASE", "MYSQL_USER", "MYSQL_PASSWORD",
        "OPENAI_API_KEY", "LUNA_MODEL",
        "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"
    ]
    for key in required_keys:
        assert key in content, f"Key {key} missing from .env.example"
