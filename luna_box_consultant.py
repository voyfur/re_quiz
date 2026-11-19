"""GPT-Luna Box Consultant for Multi-Sport Custom Boxes.

Generates tactical strategy, nutrition pacing, and physiological validation
using OpenAI (GPT Luna) with a fast rule-based fallback for:
Running, Cycling, Triathlon & Swimming, Gym & Fitness, and Hiking & Outdoor.
"""

import os
import json
import logging
import urllib.request
import urllib.error
from pathlib import Path

logger = logging.getLogger(__name__)

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TIMEOUT_SEC = 10.0


def get_api_key() -> str | None:
    key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI")
    if key:
        return key
    env_paths = [
        Path(".env"),
        Path(__file__).resolve().parent / ".env",
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


LUNA_SYSTEM_PROMPT = """Ти — Луна (GPT-Luna), головний спортивний нутриціолог та експертний консультант українського магазину Race Expert (Україна).
Ти професійно розбираєшся в біохімії спорту, енергетичному обміні, гідратації та спорядженні для:
- Бігунів (10 км, 21 км, 42 км, трейл);
- Велосипедистів (шосе, гравел, MTB, Gran Fondo);
- Триатлетів та плавців (Sprint, 70.3, 140.6, Open Water);
- Відвідувачів тренажерних залів та фітнесу (маса, рельєф, сила);
- Туристів та аутдор-ентузіастів (походи, сходження, сублімати ЇDLO).

Твоє завдання — проаналізувати індивідуальний Стартовий бокс клієнта та надати тактичний план застосування підібраних товарів.

СУВОРІ МОВНІ ВИМОГИ (ПОВНА ЗАБОРОНА РОСІЙСЬКОЇ МОВИ):
1. Вся відповідь, кожне речення, кожне слово мають бути ВИКЛЮЧНО ЧИСТОЮ ЛІТЕРАТУРНОЮ УКРАЇНСЬКОЮ МОВОЮ!
2. КАТЕГОРИЧНО ТА СУВОРО ЗАБОРОНЕНО ВИКОРИСТОВУВАТИ РОСІЙСЬКУ МОВУ АБО СУРЖИК!
3. Навіть якщо у вхідних даних або назвах є інші мови, твій текст у JSON (expert_verdict, tactical_strategy, timeline_steps, safety_badge, pro_tip) генерується ТІЛЬКИ УКРАЇНСЬКОЮ МОВОЮ.

Змістовні правила:
1. Дай чіткий покроковий таймлайн використання компонентів боксу (перед стартом/тренуванням, під час навантаження, після фінішу).
2. Обов'язково підкресли безпеку (чому саме цей набір ідеальний для шлунку, суглобів чи погоди).
3. Дай 1 унікальний практичний лайфхак від експерта (Pro-Tip).

Відповідай ВИКЛЮЧНО у валідному форматі JSON:
{
  "expert_verdict": "Стислий експертний висновок українською мовою (1-2 речення)",
  "tactical_strategy": "Детальний тактичний план розкладки сил та прийому харчування українською мовою (2-3 абзаци)",
  "timeline_steps": [
    {"timing": "Перед початком", "instruction": "Що зробити та прийняти (українською)", "product_name": "Назва товару"},
    {"timing": "Під час навантаження", "instruction": "Що зробити (українською)", "product_name": "Назва товару"},
    {"timing": "Після завершення", "instruction": "Відновлення (українською)", "product_name": "Назва товару"}
  ],
  "safety_badge": "Короткий статус безпеки українською (наприклад: '100% без кофеїну • Легко для шлунку')",
  "pro_tip": "Експертний лайфхак від Луни українською мовою"
}
"""


def consult_luna_for_box(inputs: dict, box: dict, locale: str = "uk") -> dict:
    """Consult Luna with AI, falling back to deterministic expert template if unavailable."""
    sport = inputs.get("sport") or box.get("sport") or "running"
    api_key = get_api_key()
    
    if api_key:
        try:
            items_summary = []
            for sname, items in box.get("slots", {}).items():
                for it in items:
                    p = it.get("product", {})
                    items_summary.append({
                        "slot": sname,
                        "name": p.get("name"),
                        "qty": it.get("quantity_recommended"),
                        "caffeine": p.get("caffeine"),
                        "badge": it.get("reason_badge")
                    })

            user_query = {
                "sport": sport,
                "sport_label": box.get("sport_label", sport),
                "box_title": box.get("box_title", box.get("distance_label")),
                "inputs": inputs,
                "items_in_box": items_summary
            }

            req_payload = {
                "model": OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": LUNA_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Оціни цей стартовий бокс для виду спорту '{sport}'. Відповідь надай ВИКЛЮЧНО ЧИСТОЮ УКРАЇНСЬКОЮ МОВОЮ (жодного російського слова!):\n{json.dumps(user_query, ensure_ascii=False, indent=2)}"}
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.6
            }

            req = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions",
                data=json.dumps(req_payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            )

            with urllib.request.urlopen(req, timeout=OPENAI_TIMEOUT_SEC) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
                content = json.loads(raw["choices"][0]["message"]["content"])
                
                # Strict language guard: verify NO Russian characters leak into response
                content_str = json.dumps(content, ensure_ascii=False)
                if any(c in content_str for c in "ыЫэЭъЪёЁ"):
                    logger.warning("Russian characters detected in Luna OpenAI response! Using Ukrainian expert template fallback.")
                else:
                    return {"ok": True, "source": "openai_luna", "data": content}
        except Exception as e:
            logger.warning(f"Luna OpenAI API error: {e}, using local expert fallback")

    # Sport-specific fallback templates
    if sport == "cycling":
        return {
            "ok": True,
            "source": "luna_expert_template",
            "data": {
                "expert_verdict": f"Ідеально скомпонований велобокс для дистанції {box.get('distance_label', 'заїзду')}. Забезпечує стабільний каденс та захист від судом.",
                "tactical_strategy": "На велосипеді критично підтримувати рівень 60-90 г вуглеводів на годину. Починай пити ізотонік із фляги вже з 15-ї хвилини невеликими ковтками. Крем Chamois обов'язково нанеси перед виїздом на велопамперс для повного захисту від натирання сідлом.",
                "timeline_steps": [
                    {"timing": "За 15 хв до виїзду", "instruction": "Нанести крем Chamois на памперс, заправити фляги ізотоніком.", "product_name": "Крем Chamois Butt'r + ізотонік"},
                    {"timing": "Кожні 45-50 хв", "instruction": "З'їдати 1 енергетичний батончик або гель, запивати ізотоніком.", "product_name": "Вуглеводний батончик / гель"},
                    {"timing": "Після заїзду", "instruction": "Випити порцію відновлювального протеїну або магній для зняття напруги м'язів.", "product_name": "Відновлювальний коктейль / магній"}
                ],
                "safety_badge": "Перевірено нутриціологом • Захист сідла та електролітний баланс",
                "pro_tip": "Пий за розкладом по таймеру велокомп'ютера (кожні 15 хвилин по 2-3 ковтки), навіть якщо не відчуваєш спраги!"
            }
        }
    elif sport == "triathlon":
        return {
            "ok": True,
            "source": "luna_expert_template",
            "data": {
                "expert_verdict": "Бокс підібрано з урахуванням специфіки транзитних зон T1 і T2 та мультиспортивного навантаження.",
                "tactical_strategy": "У триатлоні гонка виграється в транзитних зонах та на правильній гідратації. Гідрогелі високої плинності легко проковтнути на виході з води без запивання. Сольові капсули запобігають судомам литкових м'язів під час переходу з велоетапу на біг.",
                "timeline_steps": [
                    {"timing": "До старту на плавання", "instruction": "Обробити шию та пахви антифрикційним засобом для захисту від гідрокостюма, прийняти солі.", "product_name": "TRISWIM / захисний крем + солі"},
                    {"timing": "Транзитна зона T1", "instruction": "Прийняти 1 гідрогель, закріпити номер на поясі, взяти флягу на велоетап.", "product_name": "Гідрогель + стартовий пояс"},
                    {"timing": "Транзитка T2 та біг", "instruction": "Кофеїновий буст на заключному біговому етапі для фінішного прискорення.", "product_name": "Кофеїновий гель"},
                    {"timing": "Після фінішу", "instruction": "TRISWIM для нейтралізації хлору/солі та відновлювальний шейк.", "product_name": "TRISWIM + рекавері шейк"}
                ],
                "safety_badge": "Стандарт Ironman • Швидке проходження транзитних зон",
                "pro_tip": "Закріпи стартовий номер на спеціальному еластичному поясі: на вело номер має бути ззаду, на бігу — спереду!"
            }
        }
    elif sport == "gym":
        return {
            "ok": True,
            "source": "luna_expert_template",
            "data": {
                "expert_verdict": "Потужний силовий комплекс: енергія для тренування, захист м'язів від катаболізму та швидкий синтез білка.",
                "tactical_strategy": "Передтренувальний комплекс дає потужний нейром'язовий фокус та приплив крові (памп). BCAA під час тренування захищають м'язові волокна від мікророзривів, а сироватковий протеїн Gold Standard/Scitec протягом 30 хвилин після тренування закриває анаболічне вікно.",
                "timeline_steps": [
                    {"timing": "За 20-30 хв до залу", "instruction": "Прийняти передтренувальний комплекс або енергетичний шот, розім'ятися.", "product_name": "Передтренувальний комплекс"},
                    {"timing": "Під час тренування", "instruction": "Пити воду з BCAA або електролітами між важкими підходами.", "product_name": "BCAA у воді"},
                    {"timing": "Відразу після тренування", "instruction": "Змішати 1 мірну ложку 100% сироваткового протеїну в шейкері та випити.", "product_name": "100% Whey Protein у шейкері"},
                    {"timing": "Щоденно", "instruction": "5 г креатину моногідрату для накопичення фосфокреатину та вибухової сили.", "product_name": "Креатин моногідрат"}
                ],
                "safety_badge": "Чистий склад • Лабораторно перевірена біодоступність білка",
                "pro_tip": "Креатин найкраще запивати теплою водою з невеликою кількістю швидких вуглеводів (наприклад, виноградний сік або банан) для максимального засвоєння клітинами!"
            }
        }
    elif sport == "outdoor":
        return {
            "ok": True,
            "source": "luna_expert_template",
            "data": {
                "expert_verdict": "Легкий та поживний туристичний раціон ЇDLO. Максимум калорій при мінімальній вазі рюкзака.",
                "tactical_strategy": "У поході головне — баланс енергії та постійна гідратація. Сублімати ЇDLO готуються прямо в пакеті за 8-10 хвилин, зберігаючи всі вітаміни та натуральний смак без консервантів. Трекінгові шкарпетки із зональним ущільненням надійно бережуть стопу від мозолів.",
                "timeline_steps": [
                    {"timing": "Сніданок у таборі", "instruction": "Залити окропом сублімовану вівсянку або гранолу ЇDLO, випити дріп-каву чи чай.", "product_name": "Сніданок ЇDLO + кава/чай"},
                    {"timing": "На стежці / привал", "instruction": "Перекус горіховим батончиком або джерками ЇDLO, прийом електролітів.", "product_name": "Джерки ЇDLO / батончик + ізотонік"},
                    {"timing": "Вечеря на стоянці", "instruction": "Гарячий борщ або кус-кус ЇDLO для повного насичення та спокійного сну.", "product_name": "Гаряча страва ЇDLO"},
                    {"timing": "Перед сном", "instruction": "Прийняти магній для розслаблення натруджених ніг та захисту від судом.", "product_name": "Магній / бальзам для стоп"}
                ],
                "safety_badge": "100% натуральні інгредієнти ЇDLO • Сублімація преміум-класу",
                "pro_tip": "Не викидай пакет від сублімату — він термоізольований! Загорни його у фліску під час заварювання, і їжа пропариться швидше та залишиться гарячою навіть у мороз."
            }
        }
    else:  # running
        dist = inputs.get("distance", "21k")
        caff = inputs.get("caffeine_preference") == "boost"
        weather = inputs.get("weather", "moderate")
        
        timeline = []
        if dist == "10k":
            timeline.append({"timing": "За 15 хв до старту", "instruction": "Випити 150 мл ізотоніка та з'їсти базовий гель для заповнення глікогену.", "product_name": "Базовий енергетичний гель"})
            if caff:
                timeline.append({"timing": "6-7 км", "instruction": "Прийняти гель із кофеїном для потужного фінішного прискорення на останніх кілометрах.", "product_name": "Кофеїновий гель"})
            timeline.append({"timing": "Одразу після фінішу", "instruction": "Прийняти магній та випити ізотонік для запобігання спазмам м'язів.", "product_name": "Магній + електроліти"})
        elif dist == "21k":
            timeline.append({"timing": "За 20 хв до старту", "instruction": "Порція ізотоніка та 1 гель для стартового заряду.", "product_name": "Ізотонічний гель"})
            timeline.append({"timing": "7-8 км", "instruction": "Другий вуглеводний гель, запити кількома ковтками води на пункті харчування.", "product_name": "Енергетичний гель"})
            if caff:
                timeline.append({"timing": "15-16 км", "instruction": "Кофеїновий гель для зняття центральної втоми та підтримки темпу до фінішу.", "product_name": "Гель із кофеїном"})
            timeline.append({"timing": "Після фінішу", "instruction": "Магній + рекавері напій для відновлення м'язових волокон.", "product_name": "Рекавері та магній"})
        else:  # 42k or trail
            timeline.append({"timing": "Перед стартом", "instruction": "Нанести крем Chamois Butt'r, випити ізотонік з електролітами.", "product_name": "Крем проти натертостей"})
            timeline.append({"timing": "Кожні 35-40 хв", "instruction": "Прийом по 1 гелю, чергуючи з водою на пунктах гідратації.", "product_name": "Вуглеводні гелі"})
            if caff:
                timeline.append({"timing": "30-33 км", "instruction": "Кофеїновий буст для подолання 'марафонської стіни'.", "product_name": "Кофеїновий гель"})
            timeline.append({"timing": "Протягом 30 хв після фінішу", "instruction": "Відновлювальний шейк SiS REGO для регенерації м'язів.", "product_name": "Відновлювальний напій"})

        return {
            "ok": True,
            "source": "luna_expert_template",
            "data": {
                "expert_verdict": f"Ідеально збалансований бокс для дистанції {box.get('distance_label', dist)}. Всі компоненти перевірено на фізіологічну сумісність.",
                "tactical_strategy": f"Твій головний пріоритет на дистанції — рівномірне надходження вуглеводів без стрибків цукру. {'У спеку критично пити сольовий розчин щогодини.' if weather == 'hot' else 'Починай пити невеликими ковтками з перших кілометрів.'}",
                "timeline_steps": timeline,
                "safety_badge": "Перевірено нутриціологом • 100% сумісність компонентів",
                "pro_tip": "Ніколи не тестуй нове харчування вперше в день змагань — обов'язково протестуй 1 гель на тренуванні за тиждень до старту!"
            }
        }
