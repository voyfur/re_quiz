import json
import os

with open('test-quiz-sandbox/curated_207_audit.json') as f:
    catalog = json.load(f)

sku_map = {item['sku']: item for item in catalog}

def format_sku(sku):
    it = sku_map.get(sku)
    if not it:
        return f"- `{sku}`: [Не знайдено в каталозі]"
    return f"- **[{it['sku']}]** *{it['title']}* — **{it['price_uah']} грн**  \n  *Склад:* {it['composition']}"

print("Script base loaded successfully.")
