"""Tests for Autonomous Kit Sync and AI Tagging Pipeline."""

import os
import sys
import json
import pytest
from pathlib import Path

SANDBOX_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SANDBOX_ROOT))

from kit_extractor import MockKitExtractor, KIT_NAME_REGEX
from kit_ai_tagger import HeuristicKitTagger, LLMKitTagger
from kit_data_guard import KitDataGuard
from catalog_sync_pipeline import run_sync


def test_kit_name_regex():
    assert KIT_NAME_REGEX.search("Набір для бігу Pro")
    assert KIT_NAME_REGEX.search("Набор из 10 энергетических гелей")
    assert KIT_NAME_REGEX.search("Стартовий комплект бігуна")
    assert KIT_NAME_REGEX.search("SiS Go Variety Pack 7 шт")
    assert KIT_NAME_REGEX.search("Подарунковий бокс для спортсмена")
    assert not KIT_NAME_REGEX.search("Один гель SiS яблуко 60 мл")


def test_mock_kit_extractor():
    extractor = MockKitExtractor()
    kits = extractor.fetch_all_candidate_kits()
    assert len(kits) >= 2
    first = kits[0]
    assert "product_id" in first
    assert "sku" in first
    assert "title" in first
    assert "price_uah" in first
    assert first["price_uah"] > 0
    extractor.close()


def test_heuristic_tagger_creatine_isolation():
    tagger = HeuristicKitTagger()
    product = {
        "title": "Набір Сила та Маса: Креатин моногідрат + предтрен",
        "description": "Потужний креатин та стимулюючий передтренувальний комплекс для залу",
        "price_uah": 1400,
        "sku": "RE-CREATINE-TEST"
    }
    tagged = tagger.tag(product)
    assert tagged["has_creatine"] is True
    assert "creatine_preworkout" in tagged["component_classes"]
    assert "training" in tagged["goals"]
    assert "recovery" not in tagged["goals"]


def test_heuristic_tagger_apparel_sizing():
    tagger = HeuristicKitTagger()
    product = {
        "title": "Акційний набір бігових шкарпеток 3 пари «40–42»",
        "description": "Компресійні шкарпетки для бігу",
        "price_uah": 800,
        "sku": "RE-SOCKS-TEST"
    }
    tagged = tagger.tag(product)
    assert "apparel_footwear" in tagged["component_classes"]
    assert tagged["size_sensitive"] is True
    assert "40–42" in tagged["size_values"] or "40-42" in tagged["size_values"]
    assert "gear" in tagged["goals"]


def test_heuristic_tagger_outdoor_meals():
    tagger = HeuristicKitTagger()
    product = {
        "title": "Набір сублімованої їжі в похід (5 днів)",
        "description": "Сублімати для туризму та гірських походів, гарячі сніданки та обіди",
        "price_uah": 2100,
        "sku": "RE-MEALS-TEST"
    }
    tagged = tagger.tag(product)
    assert "dehydrated_meal" in tagged["component_classes"]
    assert "outdoors" in tagged["goals"]
    assert "hiking" in tagged["seller_activity_groups"]


def test_data_guard_apparel_sizing_rule():
    item = {"title": "Набір шкарпеток", "price_uah": 600}
    tag_data = {
        "goals": ["gear"],
        "component_classes": ["apparel_footwear"],
        "product_forms": [],
        "size_sensitive": False,
        "size_values": []
    }
    valid, issues, fixed = KitDataGuard.validate_and_fix(item, tag_data)
    assert valid is True
    assert fixed["size_sensitive"] is True
    assert any("RULE1_WARNING" in i for i in issues)


def test_data_guard_marathon_hydration_rule():
    item = {"title": "Набір на 42 км", "price_uah": 1500}
    tag_data = {
        "goals": ["running"],
        "component_classes": ["sports_accessories"],
        "product_forms": [],
        "race_formats": ["marathon"]
    }
    valid, issues, fixed = KitDataGuard.validate_and_fix(item, tag_data)
    assert valid is True
    assert "energy_nutrition" in fixed["component_classes"]
    assert any("RULE2_WARNING" in i for i in issues)


def test_data_guard_creatine_isolation_rule():
    item = {"title": "Набір Креатин Сон", "price_uah": 1200}
    tag_data = {
        "goals": ["recovery", "daily"],
        "component_classes": ["creatine_preworkout"],
        "product_forms": ["powder"],
        "has_creatine": True
    }
    valid, issues, fixed = KitDataGuard.validate_and_fix(item, tag_data)
    assert valid is True
    assert "recovery" not in fixed["goals"]
    assert "daily" not in fixed["goals"]
    assert "training" in fixed["goals"]
    assert any("RULE3_FIX" in i for i in issues)


def test_data_guard_consumables_vs_hardware_rule():
    item = {"title": "Набір шнурків та пляшка", "price_uah": 700}
    tag_data = {
        "goals": ["gear"],
        "component_classes": ["sports_accessories"],
        "product_forms": ["gel", "bars", "powder"]  # Invalid leaked food forms
    }
    valid, issues, fixed = KitDataGuard.validate_and_fix(item, tag_data)
    assert valid is True
    assert len(fixed["product_forms"]) == 0
    assert any("RULE4_FIX" in i for i in issues)


def test_data_guard_price_sanity_rule():
    item = {"title": "Безкоштовний набір", "price_uah": 0}
    tag_data = {
        "goals": ["running"],
        "component_classes": ["energy_nutrition"],
        "product_forms": ["gel"]
    }
    valid, issues, fixed = KitDataGuard.validate_and_fix(item, tag_data)
    assert valid is False
    assert any("RULE6_ERROR" in i for i in issues)


def test_pipeline_mock_dry_run():
    report = run_sync(mock=True, dry_run=True, use_llm=False)
    assert report["status"] == "SUCCESS"
    assert report["new_kits_added"] >= 1
    assert report["total_catalog_size"] >= 207
