#!/usr/bin/env python3
"""AI Consultant for Race Expert Quiz using OpenAI (GPT Luna)."""

import os
import json
import logging
import urllib.request
import urllib.error
from pathlib import Path

logger = logging.getLogger(__name__)

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
OPENAI_TIMEOUT_SEC = 12.0

def _get_api_key():
    key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI")
    if key:
        return key

    # Check local .env or /etc/race-expert-quiz
    env_paths = [
        Path(".env"),
        Path(__file__).resolve().parent.parent / ".env",
        Path("/etc/race-expert-quiz/openai.env"),
        Path("/etc/race-expert-quiz/telegram.env"),
    ]
    for p in env_paths:
        if p.exists():
            try:
                for line in p.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line.startswith("OPENAI=") or line.startswith("OPENAI_API_KEY="):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            return val
            except Exception:
                pass
    return None


SYSTEM_PROMPT = """Ти — головний спортивний нутриціолог та експертний консультант офіційного магазину Race Expert (Україна).
Твоє завдання — оцінити підібрані алгоритмом набори товарів для покупця, відсіяти семантично невідповідні та скласти професійний висновок.

Критерії суворої семантичної валідації:
1. Якщо мета «Відновлення та сон» (Восстановление и сон):
   - КАТЕГОРИЧНО ЗАБОРОНЕНО рекомендувати силовий креатин, предтренувальні комплекси чи гейнери для набору маси!
   - КАТЕГОРИЧНО ЗАБОРОНЕНО рекомендувати стимулятори, ноотропи для роботи/навчання, кордицепс, високі дози вітаміну B12 для бадьорості, комплекси для фокусу та енергії (наприклад «Фокус і продуктивність»)! Це стимулятори активності мозку та бадьорості, які прямо протипоказані перед сном та для спокійного відпочинку.
   - Для сну та відновлення підходять виключно магній, мелатонін, релакс-комплекси, ZMA, рейши, засоби для зв'язок/суглобів та вечірні протеїнові перекуси.
2. Якщо покупець обрав категорію «Спортивне харчування та батончики»:
   - Набір повинен мати ДОМІНУЮЧИЙ вміст спортивного харчування (гелі, батончики, вуглеводи, ізотоніки). Набори, де основу складають шкарпетки, пляшки та шнурки (а батончики лише як додаток), ВВАЖАЮТЬСЯ НЕВІДПОВІДНИМИ для чистого харчування!
3. Для валідних наборів:
   - Сформулюй стислий, переконливий експертний вердикт (1-2 речення).
   - Чітко виділи 2-4 головні причини, чому це ідеальний вибір.
   - Якщо ціна перевищує бюджет (Near Miss), чесно вкажи це як компроміс, але поясни вигоду більшого обсягу.

Відповідай виключно у форматі JSON за вказаною схемою."""


def consult_ai(user_request, candidates, locale="uk"):
    """Consult GPT Luna to semantically validate, score and explain candidates."""
    api_key = _get_api_key()
    if not api_key or not candidates:
        return None

    # Prepare compact candidate data
    prepared_candidates = []
    for c in candidates[:5]:
        rec = c if isinstance(c, dict) else c[0]
        ev = rec.get("matching_evidence", {})
        prepared_candidates.append({
            "catalog_row": rec.get("catalog_row"),
            "sku": rec.get("sku"),
            "title": rec.get("title"),
            "price_uah": rec.get("price_uah"),
            "composition": (rec.get("composition") or "")[:300],
            "component_classes": ev.get("component_classes", []) or rec.get("component_classes", [])
        })

    user_query = {
        "locale": locale,
        "user_request": {
            "goal": user_request.get("goal_group"),
            "component_class": user_request.get("component_class"),
            "use_scenario": user_request.get("use_scenario"),
            "use_timing": user_request.get("use_timing"),
            "max_price_uah": user_request.get("max_price_uah"),
            "shoe_size": user_request.get("shoe_size")
        },
        "candidates": prepared_candidates
    }

    user_prompt = f"""Будь ласка, оціни цих кандидатів для покупця мовою '{locale}':
{json.dumps(user_query, ensure_ascii=False, indent=2)}

Поверни JSON:
{{
  "validated_candidates": [
    {{
      "catalog_row": int,
      "is_appropriate": bool,
      "rejection_reason": str або null,
      "match_score_pct": int (0-99),
      "expert_summary": str (1-2 речення експертного висновку),
      "why_suitable": [str],
      "tradeoffs": [str]
    }}
  ],
  "consultant_note": str (стисле звернення консультанта до клієнта, якщо за вказаним бюджетом немає прямих наборів)
}}"""

    req_data = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(req_data).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=OPENAI_TIMEOUT_SEC) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
            content = json.loads(raw["choices"][0]["message"]["content"])
            return content
    except Exception as e:
        logger.warning(f"AI Consultant error (falling back to rule-based): {e}")
        return None
