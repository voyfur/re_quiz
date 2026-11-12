import sys
from pathlib import Path
ROOT = Path("test-quiz-sandbox")
sys.path.insert(0, str(ROOT))
import json
from server import _load_catalog, CATALOG_PATH, AUDIT_PATH
from draft_matcher import attach_audit_evidence, draft_recommend, DraftMatchError

raw_catalog = _load_catalog(CATALOG_PATH)
audit_data = json.load(open(AUDIT_PATH, encoding="utf-8"))
catalog = attach_audit_evidence(raw_catalog, audit_data)

print(f"Catalog loaded: {len(catalog)} sets.")
