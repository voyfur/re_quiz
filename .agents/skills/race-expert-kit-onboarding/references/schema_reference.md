# Product Kit Ingestion Schema Reference

This reference describes the JSON schema required by `ingest_kit.py` when adding a new product kit to the Race Expert quiz catalog.

---

## 1. Top-Level Kit Ingestion Object

```json
{
  "title": "string (required, e.g. 'Набір «Марафонський фініш»')",
  "price_uah": "integer (required, > 0, e.g. 1850)",
  "source_url": "string (required, valid URL on raceexpert.com.ua)",
  "sku": "string (optional or null, e.g. 'RE99101')",
  "composition": "string (required, detailed listing of kit items and counts)",
  "description": "string (optional, seller description text from page)",
  "tags": {
    "item_type": ["array of strings, e.g. 'apparel_bundle', 'snack_bundle', 'club_membership_bundle'"],
    "sport": ["optional, e.g. 'running', 'hiking'"],
    "availability": ["'in_stock' or 'out_of_stock'"]
  },
  "matching_evidence": {
    "status": "string ('candidate_direct_seller_positioning' | 'candidate_component_signal' | 'conflict_review_required')",
    "seller_families": ["array of goal families explicitly declared by the seller"],
    "component_families": ["array of goal families derived from listed component ingredients"],
    "seller_activity_groups": ["array of activity groups declared in product copy"],
    "component_activity_groups": ["array of activity groups derived from components"],
    "component_classes": ["array of component classes present in the kit"],
    "use_contexts": ["array of usage context tags (scenarios, timings, places)"],
    "race_formats": ["array of applicable race distance formats"],
    "product_forms": ["array of physical forms of goods included"],
    "size_sensitive": "boolean (true if kit contains shoe or sock size variations)",
    "size_values": [
      {
        "type": "shoe_or_sock_size",
        "value": "string (e.g. '40-42' or '43-45')"
      }
    ],
    "weather_signals": ["array of weather tags, e.g. 'cold_weather', 'summer'"],
    "conflict_notes": [
      {
        "text": "string explaining any ambiguity or discrepancy",
        "status": "'seller_context_or_positioning' or 'conflict_or_unverified_detail'",
        "source_urls": ["array of URLs"]
      }
    ]
  }
}
```

---

## 2. Field Roles & Scoring Impact

| Field | Purpose in Quiz | Scoring / Filtering Rule |
|---|---|---|
| `price_uah` | Budget filter, hints, and anchors | Hard boundary if `max_price_uah` is set; triggers Near-Miss if within +350 ₴; triggers Floor Anchor if lowest in category. |
| `seller_families` | Primary Goal Step 1 match | +20% Match Score. Enables kit to appear when buyer picks this goal. |
| `component_families` | Component-level Goal match | +15% Match Score. Corroborates physical ingredients fit the buyer's need. |
| `activity_groups` | Dynamic activity question filter | Core filter: conflicting sport eliminates kit. Universal kits (`other` / general) remain available. |
| `component_classes` | Component class question | Steering filter: conflicting product class excludes kit from exact matches. |
| `use_contexts` | Scenarios, timings & locations | Soft filter: exact match awards 100% preference points; unmentioned awards 55%; mismatch placed in relaxed pool. |
| `product_forms` | Form preferences (gel, bar, powder) | Soft filter. Mismatch drops into relaxed pool (visible via separate action). |
| `size_sensitive` + `size_values` | Numerical shoe/sock sizing | Hard filter. If user selects size 44 and kit only has 40-42, kit is completely excluded. |
| `item_type: club_membership_bundle` | Club subscription filter | Used when buyer answers "Вам потрібен набір з абонементом клубу?". |

---

## 3. Evidence Status Levels

* `candidate_direct_seller_positioning`: Page title and text explicitly declare the purpose of the kit (e.g., "Спеціальний комплект для марафонців"). Preferred baseline.
* `candidate_component_signal`: Seller text is generic, but physical products (e.g. SiS gels, Myprotein shaker, compression socks) clearly belong to specific athletic use cases.
* `conflict_review_required`: Kit description contradicts bulleted composition (e.g. text mentions magnesium, but bullet points omit it). Incurs a -5% confidence penalty and adds a visible review note on the card.
