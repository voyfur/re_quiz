import os
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_requirements_file_exists():
    req_path = ROOT / "requirements.txt"
    assert req_path.exists(), "requirements.txt must exist"
    content = req_path.read_text(encoding="utf-8")
    assert "pytest" in content

def test_dockerfile_structure():
    df_path = ROOT / "Dockerfile"
    assert df_path.exists(), "Dockerfile must exist"
    content = df_path.read_text(encoding="utf-8")
    assert "FROM python:3.12-slim" in content
    assert "WORKDIR /app" in content
    assert "EXPOSE 8000" in content
    assert 'CMD ["python3", "server.py"]' in content

def test_docker_compose_structure():
    dc_path = ROOT / "docker-compose.yml"
    assert dc_path.exists(), "docker-compose.yml must exist"
    content = dc_path.read_text(encoding="utf-8")
    assert "8000" in content
    assert "restart: always" in content
