"""Kit Extractor for Race Expert Quiz.

Fetches product sets/kits from OpenCart MySQL database.
Handles readonly user permissions and identifies sets precisely.
"""

import os
import re
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)

KIT_NAME_PATTERNS = [
    r"набір",
    r"набор",
    r"\bсет\b",
    r"\bкомплект\b",
    r"variety pack",
    r"starter kit",
    r"\bбокс\b"
]

KIT_NAME_REGEX = re.compile("|".join(KIT_NAME_PATTERNS), re.IGNORECASE)


class OpenCartKitExtractor:
    """Extracts candidate kit products from OpenCart database."""

    def __init__(self, stock_checker=None):
        if stock_checker is None:
            from stock_checker import StockChecker
            self.stock_checker = StockChecker()
        else:
            self.stock_checker = stock_checker

    def fetch_all_candidate_kits(self, limit: Optional[int] = None, allowed_product_ids: Optional[set] = None) -> List[Dict[str, Any]]:
        """Fetch candidate kits from oc_product and oc_product_description."""
        from stock_checker import _mysql_query

        sock = self.stock_checker._ensure_connection()
        limit_clause = f"LIMIT {int(limit)}" if limit else ""
        
        sql = f"""
        SELECT 
            p.product_id,
            p.model,
            p.sku,
            p.price,
            p.quantity,
            p.status,
            p.image,
            p.date_modified,
            pd.language_id,
            pd.name,
            pd.description
        FROM oc_product p
        JOIN oc_product_description pd ON p.product_id = pd.product_id
        WHERE p.status = 1
          AND (
            pd.name LIKE '%набір%' 
            OR pd.name LIKE '%набор%' 
            OR pd.name LIKE '%комплект%' 
            OR pd.name LIKE '%variety pack%'
            OR pd.name LIKE '% сет %' 
            OR pd.name LIKE 'Сет %'
            OR pd.name LIKE '«Сет %'
            OR p.model LIKE 'Nabir_%'
          )
        ORDER BY p.product_id ASC
        {limit_clause}
        """
        
        rows = _mysql_query(sock, sql)
        
        # Group by product_id
        by_id: Dict[str, Dict[str, Any]] = {}
        for r in rows:
            pid = str(r.get("product_id"))
            if pid not in by_id:
                raw_price = float(r.get("price") or 0.0)
                by_id[pid] = {
                    "product_id": pid,
                    "model": (r.get("model") or "").strip(),
                    "sku": (r.get("sku") or r.get("model") or "").strip(),
                    "price_uah": round(raw_price),
                    "quantity": int(r.get("quantity") or 0),
                    "in_stock": int(r.get("quantity") or 0) > 0,
                    "status": int(r.get("status") or 0),
                    "image": r.get("image") or "",
                    "date_modified": str(r.get("date_modified") or ""),
                    "names": {},
                    "descriptions": {},
                }
            
            lang_id = str(r.get("language_id"))
            name = (r.get("name") or "").strip()
            desc = (r.get("description") or "").strip()
            by_id[pid]["names"][lang_id] = name
            by_id[pid]["descriptions"][lang_id] = desc

        results = []
        for pid, data in by_id.items():
            name_uk = data["names"].get("1") or data["names"].get("3") or ""
            name_ru = data["names"].get("2") or ""
            primary_name = name_uk or name_ru or (list(data["names"].values())[0] if data["names"] else "")
            
            desc_uk = data["descriptions"].get("1") or data["descriptions"].get("3") or ""
            desc_ru = data["descriptions"].get("2") or ""
            primary_desc = desc_uk or desc_ru or (list(data["descriptions"].values())[0] if data["descriptions"] else "")
            
            is_kit_name = bool(KIT_NAME_REGEX.search(primary_name))
            is_kit_sku = data["model"].startswith("Nabir_")
            
            if is_kit_name or is_kit_sku:
                results.append({
                    "product_id": data["product_id"],
                    "model": data["model"],
                    "sku": data["sku"] or data["model"],
                    "title": primary_name,
                    "title_uk": name_uk or primary_name,
                    "title_ru": name_ru or primary_name,
                    "description": primary_desc,
                    "price_uah": data["price_uah"],
                    "quantity": data["quantity"],
                    "in_stock": data["in_stock"],
                    "status": data["status"],
                    "image": data["image"],
                    "date_modified": data["date_modified"],
                    "source_url": f"https://raceexpert.com.ua/index.php?route=product/product&product_id={data['product_id']}"
                })

        if allowed_product_ids is not None:
            before_cnt = len(results)
            results = [r for r in results if str(r.get("product_id")) in allowed_product_ids]
            logger.info(f"Filtered by 'За потребами' category: {before_cnt} -> {len(results)} kits.")
        return results

    def close(self):
        if self.stock_checker:
            self.stock_checker.close()


class MockKitExtractor:
    """Mock extractor for offline testing without DB access."""

    def __init__(self, sample_records: Optional[List[Dict[str, Any]]] = None):
        if sample_records is not None:
            self.sample_records = sample_records
        else:
            self.sample_records = [
                {
                    "product_id": "9901",
                    "model": "RE-TEST-MARATHON",
                    "sku": "RE-TEST-MARATHON",
                    "title": "Набір спортивного харчування «Марафон Pro 42 км»: 8 гелів SiS + ізотонік Hydria + сольові капсули",
                    "title_uk": "Набір спортивного харчування «Марафон Pro 42 км»: 8 гелів SiS + ізотонік Hydria + сольові капсули",
                    "title_ru": "Набор спортивного питания «Марафон Pro 42 км»: 8 гелей SiS + изотоник Hydria + солевые капсулы",
                    "description": "Повний стартовий комплект вуглеводів та солей на марафонську дистанцію 42 км. Включає 8 вуглеводних ізотонічних гелів з електролітами.",
                    "price_uah": 1250,
                    "quantity": 10,
                    "in_stock": True,
                    "status": 1,
                    "image": "catalog/marathon_pro.jpg",
                    "date_modified": "2026-11-13 08:00:00",
                    "source_url": "https://raceexpert.com.ua/index.php?route=product/product&product_id=9901"
                },
                {
                    "product_id": "9902",
                    "model": "RE-TEST-SOCKS",
                    "sku": "RE-TEST-SOCKS",
                    "title": "Набір компресійних бігових шкарпеток Race Expert «Розмір M (40-42)»",
                    "title_uk": "Набір компресійних бігових шкарпеток Race Expert «Розмір M (40-42)»",
                    "title_ru": "Набор компрессионных беговых носков Race Expert «Размер M (40-42)»",
                    "description": "Комплект з трьох пар компресійних шкарпеток для захисту стопи під час тривалого бігу. Розмір 40-42.",
                    "price_uah": 890,
                    "quantity": 5,
                    "in_stock": True,
                    "status": 1,
                    "image": "catalog/socks_m.jpg",
                    "date_modified": "2026-11-13 08:00:00",
                    "source_url": "https://raceexpert.com.ua/index.php?route=product/product&product_id=9902"
                }
            ]

    def fetch_all_candidate_kits(self, limit: Optional[int] = None, allowed_product_ids: Optional[set] = None) -> List[Dict[str, Any]]:
        if limit:
            return self.sample_records[:limit]
        return list(self.sample_records)

    def close(self):
        pass
