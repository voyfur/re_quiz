import json
import sys

with open('test-quiz-sandbox/curated_207_audit.json') as f:
    catalog_items = json.load(f)

sku_lookup = {item['sku']: item for item in catalog_items}

def format_sku(sku):
    item = sku_lookup.get(sku)
    if not item:
        return f"`{sku}` (Item not in catalog)"
    return f"**[{sku}]** *{item['title']}* — **{item['price_uah']} грн** (Склад: {item['composition']})"

print("Helper ready.")
