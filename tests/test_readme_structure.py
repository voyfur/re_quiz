from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_readme_exists_and_contains_deployment_guide():
    readme_path = ROOT / "README.md"
    assert readme_path.exists(), "README.md must exist"
    content = readme_path.read_text(encoding="utf-8")
    
    required_sections = [
        "Race Expert Quiz & Starter Box Builder",
        "docker compose up -d",
        "systemd",
        "location /quiz/",
        "proxy_pass",
        "OCSESSID",
        "quiz_cart.php",
        "add_bulk",
        "curl -X POST",
        "/api/generate-sport-box"
    ]
    for sec in required_sections:
        assert sec in content, f"Section or directive '{sec}' missing in README.md"
