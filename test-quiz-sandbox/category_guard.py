"""Category Guard for Race Expert Quiz.

Ensures only products strictly belonging to the official category
"За потребами" (https://raceexpert.com.ua/nabori/po-potrebam/)
are admitted into the quiz catalog synchronization pipeline.
"""

import re
import json
import logging
import urllib.request
from typing import Set

logger = logging.getLogger(__name__)

CATEGORY_URL = "https://raceexpert.com.ua/nabori/po-potrebam/"


def fetch_category_allowed_product_ids(base_url: str = CATEGORY_URL) -> Set[str]:
    """Crawl active category page to get all official product IDs in 'За потребами'."""
    allowed_ids = set()
    page = 1
    
    while True:
        url = f"{base_url}?page={page}" if page > 1 else base_url
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "RaceExpertCategorySync/2.0"}
        )
        try:
            with urllib.request.urlopen(req, timeout=8.0) as resp:
                html = resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            logger.warning(f"Category page {page} fetch error: {e}")
            break

        # Extract content_ids from marketing json
        m = re.search(
            r'\"content_name\":\s*\"(?:\\u0417\\u0430\s*\\u043f\\u043e\\u0442\\u0440\\u0435\\u0431\\u0430\\u043c\\u0438|За потребами)\".*?\"content_ids\":\s*(\[.*?\])',
            html
        )
        if m:
            try:
                page_ids = set(json.loads(m.group(1)))
            except Exception:
                page_ids = set()
        else:
            page_ids = set(re.findall(r'https://raceexpert.com.ua/([0-9]{3,6})-[a-z0-9-]+', html))

        new_ids = page_ids - allowed_ids
        if not new_ids:
            break
            
        allowed_ids.update(page_ids)
        page += 1

    logger.info(f"Fetched {len(allowed_ids)} official product IDs from 'За потребами'.")
    return allowed_ids
