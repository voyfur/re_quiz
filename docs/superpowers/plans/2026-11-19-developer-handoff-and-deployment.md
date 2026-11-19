# Developer Handoff and Production Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare the Race Expert Quiz and Box Builder repository for handoff to the store's external developer on GitHub with full Dockerization, OpenCart bulk cart integration controller, environment templates, complete deployment documentation, and verified test suites.

**Architecture:** The service runs as a self-contained Python 3.12 HTTP server serving pre-calculated static JSON sport catalogs and dynamic matching algorithms with sub-5ms latency. A lightweight Docker container and docker-compose deployment isolate the runtime, while an Nginx reverse proxy on `raceexpert.com.ua/quiz/` handles Same-Origin requests and transparently forwards OpenCart session cookies (`OCSESSID`). OpenCart cart integration is handled by a custom atomic bulk-add PHP controller (`api/quiz_cart/add_bulk`).

**Tech Stack:** Python 3.12, Docker, Docker Compose, Nginx, PHP (OpenCart 3.x / 4.x), Vanilla JS / Tailwind CSS (CDN), pytest.

**Spec:** `wiki/projects/quiz-developer-deployment-and-opencart-integration-guide.md` and `raw/sources/2026-11-19-programmer-handoff-and-deployment-preparation.md`.

## Global Constraints

- Python runtime version floor: Python 3.10+ (Docker image pinned to `python:3.12-slim`).
- Zero external runtime Python dependencies required for the core server (`server.py` uses standard library `http.server.ThreadingHTTPServer`).
- OpenCart integration must support atomic batch addition of products to avoid multiple HTTP calls.
- Port standard: 8000 (configurable via `PORT` environment variable).
- Nginx reverse proxy pattern: `raceexpert.com.ua/quiz/` preserving `Host`, `X-Real-IP`, and OpenCart session cookies.
- All 343+ test scenarios must pass regression testing with 100% success rate.
- No sensitive data, API keys, or private environment variables committed to git.

## Review Focus

1. **Docker container file inclusion:** All required engine files (`runner_box_engine.py`, `multi_sport_engine.py`, `stock_checker.py`, `luna_box_consultant.py`), JSON catalogs (`running_catalog.json`, `cycling_catalog.json`, etc.), and frontend assets (`public/`) must be copied into `/app`.
2. **OpenCart Session & Cookie handling:** Bulk cart controller must execute within the buyer's active OpenCart session and invalidate shipping/payment cache so cart totals reflect the newly added box immediately.
3. **Environment fallback:** `server.py` and engines must safely handle missing optional environment variables (e.g. OpenAI key for Luna, MySQL for live stock check) without crashing.
4. **Clean Git footprint:** `.gitignore` must strictly exclude `.env`, `.env.*`, `__pycache__`, `*.pyc`, `*.log`, `.pytest_cache`, `.DS_Store`, and system artifacts.
5. **Test harness unification:** `pytest.ini` must discover both sandbox tests (110) and root multi-sport / runner tests (343) consistently.

---

### Task 1: Docker Environment Setup

**Files:**
- Create: `Dockerfile`
- Create: `docker-compose.yml`
- Create: `requirements.txt`
- Test: `tests/test_docker_config.py`

**Interfaces:**
- Consumes: `server.py`, `public/`, `*.json`, `runner_box_engine.py`, `multi_sport_engine.py`, `stock_checker.py`, `luna_box_consultant.py`.
- Produces: Runnable Docker container listening on port 8000 with healthcheck and graceful shutdown.

- [ ] **Step 1: Write test for Docker and dependency configuration**

Create `tests/test_docker_config.py` to verify `Dockerfile`, `docker-compose.yml`, and `requirements.txt` exist and contain required directives:
```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_docker_config.py -v`
Expected: FAIL with missing files.

- [ ] **Step 3: Create `requirements.txt`**

Create `requirements.txt` documenting standard library server usage and developer test dependencies:
```text
# Race Expert Quiz & Starter Box Builder
# Core server runs on Python standard library (http.server) with zero external runtime dependencies.

# Optional / Testing dependencies:
pytest>=8.0.0
pytest-asyncio>=0.23.0
```

- [ ] **Step 4: Create production-ready `Dockerfile`**

Create `Dockerfile` using `python:3.12-slim`:
```dockerfile
FROM python:3.12-slim

# Prevent python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Europe/Kyiv \
    PORT=8000 \
    BIND_HOST=0.0.0.0

WORKDIR /app

# Install system utilities if needed for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and JSON catalogs
COPY server.py runner_box_engine.py multi_sport_engine.py stock_checker.py luna_box_consultant.py ./
COPY *.json ./
COPY public/ ./public/

# Expose standard application port
EXPOSE 8000

# Container healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/ || exit 1

CMD ["python3", "server.py"]
```

- [ ] **Step 5: Create `docker-compose.yml`**

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  quiz-app:
    build: .
    container_name: raceexpert-quiz
    restart: always
    ports:
      - "${PORT:-8000}:8000"
    environment:
      - PORT=8000
      - BIND_HOST=0.0.0.0
      - TZ=Europe/Kyiv
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://127.0.0.1:8000/"]
      interval: 30s
      timeout: 5s
      retries: 3
```

- [ ] **Step 6: Run test to verify it passes**

Run: `pytest tests/test_docker_config.py -v`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add requirements.txt Dockerfile docker-compose.yml tests/test_docker_config.py
git commit -m "feat(deploy): add production Dockerfile, docker-compose, and requirements"
```

---

### Task 2: OpenCart Bulk Add Controller Module

**Files:**
- Create: `integrations/opencart/catalog/controller/api/quiz_cart.php`
- Create: `tests/test_opencart_controller_structure.py`

**Interfaces:**
- Consumes: HTTP POST request with JSON payload `{"items": [{"product_id": int, "quantity": int, "option": {}}]}`.
- Produces: Standard OpenCart JSON response with `success`, `added_items`, `total_items`, `redirect`.

- [ ] **Step 1: Write test for OpenCart controller structure**

Create `tests/test_opencart_controller_structure.py`:
```python
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_opencart_controller_exists_and_contains_logic():
    controller_path = ROOT / "integrations" / "opencart" / "catalog" / "controller" / "api" / "quiz_cart.php"
    assert controller_path.exists(), "quiz_cart.php controller must exist"
    
    code = controller_path.read_text(encoding="utf-8")
    assert "ControllerApiQuizCart" in code
    assert "public function add_bulk()" in code
    assert "$this->cart->add(" in code
    assert "application/json" in code
    assert "shipping_methods" in code
    assert "payment_methods" in code
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_opencart_controller_structure.py -v`
Expected: FAIL (file missing).

- [ ] **Step 3: Implement `quiz_cart.php` in `integrations/opencart/catalog/controller/api/quiz_cart.php`**

Write standard, robust OpenCart 3.x/4.x compatible PHP controller:
```php
<?php
/**
 * Race Expert Quiz - OpenCart Bulk Cart Controller
 *
 * Allows adding multiple products from a starter/training box into the buyer's
 * current OpenCart session in a single atomic HTTP request.
 *
 * Route: index.php?route=api/quiz_cart/add_bulk
 */
class ControllerApiQuizCart extends Controller {
    public function add_bulk() {
        $this->response->addHeader('Content-Type: application/json');
        $json = array();

        // Retrieve raw JSON body
        $raw_input = file_get_contents('php://input');
        $data = json_decode($raw_input, true);

        if (!empty($data['items']) && is_array($data['items'])) {
            $added_count = 0;

            foreach ($data['items'] as $item) {
                $product_id = isset($item['product_id']) ? (int)$item['product_id'] : 0;
                $quantity = isset($item['quantity']) ? (int)$item['quantity'] : 1;
                $option = isset($item['option']) && is_array($item['option']) ? $item['option'] : array();

                if ($product_id > 0 && $quantity > 0) {
                    // Call standard OpenCart cart add method
                    $this->cart->add($product_id, $quantity, $option);
                    $added_count++;
                }
            }

            // Invalidate calculated shipping & payment cache in session
            unset($this->session->data['shipping_methods']);
            unset($this->session->data['shipping_method']);
            unset($this->session->data['payment_methods']);
            unset($this->session->data['payment_method']);

            $json['success'] = true;
            $json['added_items'] = $added_count;
            $json['total_items'] = $this->cart->countProducts();
            $json['redirect'] = $this->url->link('checkout/cart', '', true);
        } else {
            $json['success'] = false;
            $json['error'] = 'Порожній або некоректний список товарів для додавання';
        }

        $this->response->setOutput(json_encode($json));
    }
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_opencart_controller_structure.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add integrations/opencart/catalog/controller/api/quiz_cart.php tests/test_opencart_controller_structure.py
git commit -m "feat(opencart): add bulk cart controller quiz_cart.php for atomic cart population"
```

---

### Task 3: Environment Configuration Template (`.env.example`)

**Files:**
- Create: `.env.example`
- Test: `tests/test_env_example.py`

**Interfaces:**
- Consumes: Configuration keys used in `server.py`, `stock_checker.py`, `luna_box_consultant.py`.
- Produces: Fully annotated `.env.example` file with production guidance in Ukrainian.

- [ ] **Step 1: Write test for `.env.example`**

Create `tests/test_env_example.py`:
```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_env_example.py -v`
Expected: FAIL (.env.example missing).

- [ ] **Step 3: Create `.env.example`**

Write `.env.example` with clear sections:
```env
# ==============================================================================
# Race Expert Quiz & Starter Box Builder - Environment Configuration
# Скопіюйте цей файл у .env та заповніть актуальні параметри
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Параметри HTTP-сервера
# ------------------------------------------------------------------------------
PORT=8000
BIND_HOST=0.0.0.0
BASE_URL=https://raceexpert.com.ua

# ------------------------------------------------------------------------------
# 2. Інтеграція з кошиком OpenCart
# ------------------------------------------------------------------------------
# Стандартний нативний ендпоінт додавання по 1 товару (послідовні POST-запити)
OPENCART_CART_ENDPOINT=/index.php?route=checkout/cart/add

# Рекомендований пакетний ендпоінт (додавання всього боксу в 1 клік)
OPENCART_BULK_ENDPOINT=/index.php?route=api/quiz_cart/add_bulk

# URL сторінки перегляду кошика для редиректу покупця
OPENCART_VIEW_CART_URL=/index.php?route=checkout/cart

# ------------------------------------------------------------------------------
# 3. Підключення до MySQL OpenCart (для фонової синхронізації та перевірки наявності)
# ------------------------------------------------------------------------------
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=raceexpertcomua
MYSQL_USER=raceexpert_readonly
MYSQL_PASSWORD=your_secure_mysql_password_here

# ------------------------------------------------------------------------------
# 4. ШІ-консультант Луна (GPT консультація за сформованим боксом)
# ------------------------------------------------------------------------------
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
LUNA_MODEL=gpt-4o-mini

# ------------------------------------------------------------------------------
# 5. Сповіщення в Telegram (опціонально: отримання заявок консультацій)
# ------------------------------------------------------------------------------
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_env_example.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .env.example tests/test_env_example.py
git commit -m "feat(config): add annotated .env.example configuration template"
```

---

### Task 4: Store Developer `README.md` & Deployment Guide

**Files:**
- Create: `README.md`

**Interfaces:**
- Consumes: Documentation in `wiki/projects/quiz-developer-deployment-and-opencart-integration-guide.md`.
- Produces: Professional Markdown README for the store developer on GitHub.

- [ ] **Step 1: Write `README.md`**

Include:
- Project overview & capabilities (5 sports, < 5ms calculation, single gel brand rule, budget optimization, interactive deselection).
- Architecture diagram and file map.
- Quick start with Docker (`docker compose up -d`).
- Alternative quick start via systemd (`quiz.service`).
- Complete Nginx reverse proxy configuration block for `raceexpert.com.ua/quiz/` explaining Same-Origin, `OCSESSID` session preservation, and zero-CORS.
- OpenCart bulk cart controller installation instructions.
- Verification examples with `curl` for all key endpoints.

- [ ] **Step 2: Verify `README.md` readability and link references**

Check syntax, markdown headings, code block formatting, and curl examples.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add comprehensive developer README and deployment guide for GitHub handoff"
```

---

### Task 5: Security, Repository Cleanup (`.gitignore`) and Test Suite Unification

**Files:**
- Modify: `.gitignore`
- Modify: `pytest.ini`
- Modify: `test_20_runner_scenarios.py`

**Interfaces:**
- Consumes: All tests across root and sandbox directories.
- Produces: 100% clean test execution via unified `pytest` run and leak-proof `.gitignore`.

- [ ] **Step 1: Update `.gitignore`**

Ensure `.gitignore` contains comprehensive exclusions:
```gitignore
# Secrets and environment configs
.env
.env.*
!.env.example

# Python runtime and caches
__pycache__/
*.py[cod]
*$py.class
*.so
.pytest_cache/
.coverage
htmlcov/

# Logs and runtime databases
*.log
logs/
*.pid

# IDE and OS files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
.idea/
.vscode/

# Antigravity / Agent internals
.system_generated/
.playwright-cli/
```

- [ ] **Step 2: Wire `test_20_runner_scenarios.py` into pytest**

Wrap the runner in `test_20_runner_scenarios.py` with standard `def test_20_runner_scenarios():` so pytest collects and executes it automatically.

- [ ] **Step 3: Update `pytest.ini` to discover root and sandbox tests**

Set:
```ini
[pytest]
pythonpath = test-quiz-sandbox .
testpaths = tests test-quiz-sandbox/tests .
python_files = test_*.py *_test.py
```

- [ ] **Step 4: Run full regression test suite**

Run: `pytest -v`
Expected: ALL test suites pass (110 sandbox tests + 323 multi-sport/runner tests + 1 20-scenario runner test + 3 new deploy tests = 437 tests total).

- [ ] **Step 5: Commit**

```bash
git add .gitignore pytest.ini test_20_runner_scenarios.py
git commit -m "chore: unify test suite in pytest.ini, wire 20 scenarios, and harden .gitignore"
```

---

### Task 6: Final Verification & Wiki Knowledge Handoff

**Files:**
- Modify: `wiki/session-handoff.md`
- Modify: `wiki/index.md`
- Run: `python3 .agents/skills/llm-wiki-session-memory/scripts/rebuild_content_index.py .`
- Run: `python3 .agents/skills/llm-wiki-session-memory/scripts/lint_content.py .`
- Run: `python3 .agents/skills/llm-wiki-session-memory/scripts/lint_memory.py .`

- [ ] **Step 1: Update `wiki/session-handoff.md`**

Record completion of all handoff files (`Dockerfile`, `docker-compose.yml`, `quiz_cart.php`, `.env.example`, `README.md`, `.gitignore`, tests passing).

- [ ] **Step 2: Rebuild and lint Wiki indexes**

Run:
```bash
python3 .agents/skills/llm-wiki-session-memory/scripts/rebuild_content_index.py .
python3 .agents/skills/llm-wiki-session-memory/scripts/lint_content.py .
python3 .agents/skills/llm-wiki-session-memory/scripts/lint_memory.py .
```
Expected: All linter checks pass with 0 errors.

- [ ] **Step 3: Commit**

```bash
git add wiki/
git commit -m "docs(wiki): update session handoff and rebuild content index for developer handoff"
```
