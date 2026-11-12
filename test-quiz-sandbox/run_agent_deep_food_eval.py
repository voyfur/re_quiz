#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QA Deep Food Specialist: 100 Dedicated Buyer Test Scenarios & Evaluation for 'food' Goal."""

import json
import os
import sys
from pathlib import Path

# Add sandbox to sys.path
SANDBOX_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SANDBOX_DIR.parent
sys.path.insert(0, str(SANDBOX_DIR))

from draft_matcher import attach_audit_evidence, draft_recommend, DraftMatchError

CATALOG_PATH = SANDBOX_DIR / "catalog.json"
AUDIT_PATH = PROJECT_ROOT / "wiki" / "projects" / "quiz-set-audit.json"
OUTPUT_JSON = SANDBOX_DIR / "agent_deep_food_100_tests.json"
OUTPUT_REPORT = SANDBOX_DIR / "agent_deep_food_report.md"

def load_environment():
    cat = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    catalog = attach_audit_evidence(cat, audit)
    return catalog

print("Environment loader ready.")
