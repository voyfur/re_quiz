import json
import os

with open('test-quiz-sandbox/curated_207_audit.json') as f:
    catalog = json.load(f)

sku_map = {item['sku']: item for item in catalog}

def sku_line(sku):
    it = sku_map.get(sku)
    if not it:
        return f"- `{sku}` (Not in catalog)"
    return f"- **[{it['sku']}]** *{it['title']}* — **{it['price_uah']} грн**  \n  *Склад:* {it['composition']}"

output_file = 'test-quiz-sandbox/production_ai_question_system.md'

with open(output_file, 'w', encoding='utf-8') as out:
    def w(text=""):
        out.write(text + "\n")

    # Header
    w("# Production AI Question System: Clinical & Athletic Conversational Architecture (9 Categories)")
    w("**Role:** Lead Conversational Architect & Clinical AI Question Designer for Race Expert")
    w("**Foundational Corpus:** 900 End-to-End Stress Test Scenarios Across 207 Catalog Sets")
    w("**Guiding Philosophy:** Rigorous AI-Evaluated Goal Congruence (*«Подходит / Не подходит к ключевой цели»*)")
    w("**Document Status:** Production Master Reference | Zero Dead Ends Guaranteed")
    w()
    w("---")
    w()

    # SECTION 1
    w("# 1. Executive Manifesto & The «Подходит / Не подходит» AI Philosophy")
    w()
    w("## 1.1. The User's Foundational Directive")
    w("> *«То есть агенты должны будут руководствоваться такой логикой. К примеру: „Для какой цели вы выбираете набор?“ Заходят, например, на „Гидратация“: это электролиты.*  ")
    w("> *Вот тут есть вопрос: какой ключевой тип товара?*  ")
    w("> *- Спортивне харчування*  ")
    w("> *- Ізотоніки та електроліти*  ")
    w("> *- Спортивний аксесуар: это пляшка*  ")
    w("> *Тут должен возникать вопрос: подходит ли это для ключевой цели? Спортивные аксессуары и фляжки подходят для цели „Гидратация“? Это электролиты?*  ")
    w("> *Это вот как один пример. Тут нужна агентская система, тут нужен агент, который будет задавать себе вопрос: „Подходит, не подходит?“ и составлять кучу вопросов, таким образом, чтобы это все идеально ложилось на квиз. Где надо 5 вопросов, где надо 10 вопросов. То есть это должны быть вопросы, чтобы максимально дать человеку то, что он хочет, и использовать здесь только логику искусственного интеллекта.»*")
    w()
    w("## 1.2. The 4 Inviolable Golden Rules of Goal Congruence")
    w()
    w("1. **The Primary Deliverable Invariant (No Fake Substitutions):**  ")
    w("   When a buyer enters a category with a physiological need (e.g., Hydration, Recovery, Running Endurance), they **MUST receive the active physiological agent** (electrolytes, restorative minerals, energy fuels). An accessory (such as a water bottle, soft flask, towel, socks, or shaker) can **NEVER be substituted as the sole deliverable** for a nutritional or physiological need. Accessories may ONLY be offered as **companion bundles** (e.g., *«Electrolytes + Soft Flask Bundle»*) or when the user explicitly requests gear alone in the dedicated Gear category.")
    w()
    w("2. **Strict Negative Constraints & Domain Banishment (Zero Toxic Cross-Contamination):**  ")
    w("   Grounded in our 900 stress tests, algorithmic classification errors led to severe pharmacological absurdities. Under this AI Question System, the following strict exclusions are hardcoded into every question branch:")
    w("   - **Creatine & Pre-workout Stimulants** are permanently BANISHED from Recovery (Sleep), Daily Health, Endurance Running, and Gear.")
    w("   - **Sedatives & Neuro-relaxants** (ZMA, GABA, Melatonin, 5-HTP) are BANISHED from Gym Pre-Workout, Daytime Energy, and Race Morning.")
    w("   - **Dehydrated Hot Camping Meals (ЇDLO)** are strictly distinguished from sweet endurance running gels and gym snack bars.")
    w("   - **Psychoactive & Functional Mushrooms (Amanita muscaria / Lion's Mane)** require explicit, unbundled informed consent — NEVER recommended covertly or defaulted.")
    w("   - **Socks & Apparel** are BANISHED as standalone results from Hydration, Food, and Recovery.")
    w()
    w("3. **Physical Sizing Integrity (Shoe Size Precision vs. Zero-Sizing Safety):**  ")
    w("   Whenever a set contains socks, calf sleeves, or wearable textiles, a precise shoe size verification question (35–37, 38–40, 40–42, 43–45, 46–48) is **MANDATORY**. If the buyer is choosing a gift or does not know the shoe size, the quiz MUST divert them to **zero-sizing items** (Sharpey towels, medal hangers, electrolytes, nutrition) to prevent delivery of unwearable gear.")
    w()
    w("4. **Adaptive Diagnostic Flow (5 to 10 Questions):**  ")
    w("   Instead of a shallow 3-question filter, each category features an adaptive sequence of 8 to 10 deep, clinically and athletically calibrated questions that replicate an empathetic elite coach and sports doctor. Questions cover core need, modality, component bundle composition, form factor, sizing, physiological constraints, supply duration, and budget anchors.")
    w()
    w("---")
    w()

print("Manifesto section written.")
