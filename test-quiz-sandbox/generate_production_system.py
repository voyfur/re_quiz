import json
import os

with open('test-quiz-sandbox/curated_207_audit.json') as f:
    catalog_items = json.load(f)

sku_lookup = {item['sku']: item for item in catalog_items}

print(f"Loaded {len(catalog_items)} sets for grounding.")
