"""Build a test-only JSON catalog from the maintained 206-set Wiki analysis."""

import argparse
import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = PROJECT_ROOT / "wiki" / "projects" / "race-expert-need-sets-206-analysis.md"
OUTPUT_PATH = Path(__file__).resolve().parent / "catalog.json"
SNAPSHOT_DATE = "2026-11-06"

HEADING_RECORD = re.compile(r"^### (\d+)\.\s+(.+)$")
NUMBERED_RECORD = re.compile(r"^(\d+)\.\s+\*\*(.+?)\*\*\s+—\s+(.+)$")
BULLET_RECORD = re.compile(r"^-\s+\*\*(\d+)\s+·\s+(.+?)\s+·\s+(.+?)\*\*")
TAG_VALUE = re.compile(r"([a-z][a-z0-9_]*)\s*:\s*([a-z0-9_-]+)")


def _record_start(line):
    match = HEADING_RECORD.match(line)
    if match:
        row = int(match.group(1))
        identity, separator, title = match.group(2).partition(" — ")
        if separator:
            return row, identity.strip(), title.strip()

    match = NUMBERED_RECORD.match(line)
    if match:
        row = int(match.group(1))
        identity = match.group(2).strip()
        title = match.group(3).split(". Цена каталога", 1)[0].strip().rstrip(".")
        return row, identity, title

    match = BULLET_RECORD.match(line)
    if match:
        row = int(match.group(1))
        identity = match.group(2).strip()
        title = match.group(3).split(" · ", 1)[0].strip().rstrip(".")
        title = title.strip("\"“”")
        return row, identity, title

    return None


def _tag_map(block):
    tags = {}
    for match in re.finditer(r"(?:\*\*)?Теги:(?:\*\*)?\s*([^\n]+)", block):
        for namespace, value in TAG_VALUE.findall(match.group(1)):
            tags.setdefault(namespace, [])
            if value not in tags[namespace]:
                tags[namespace].append(value)
    return tags


def _extract_after_label(block, label_pattern, stop_patterns):
    label = re.search(label_pattern, block, re.IGNORECASE)
    if not label:
        return ""

    start = label.end()
    end = len(block)
    remainder = block[start:]
    for pattern in stop_patterns:
        match = re.search(pattern, remainder, re.IGNORECASE)
        if match:
            end = min(end, start + match.start())
    return re.sub(r"\s+", " ", block[start:end]).strip(" \t\r\n;,.—")


def _parse_record(row, identity, title, block):
    tags = _tag_map(block)
    price_values = tags.get("price", [])
    price_match = re.search(r"^(\d+)_uah$", price_values[0]) if price_values else None
    if not price_match:
        raise ValueError("Catalog row {} has no parseable price tag".format(row))

    source_match = re.search(r"\]\((https?://[^)]+)\)", block)
    if not source_match:
        raise ValueError("Catalog row {} has no source URL".format(row))

    composition = _extract_after_label(
        block,
        r"(?:\*\*)?Состав(?:\s+набора)?:(?:\*\*)?\s*",
        [
            r"\.\s*Назначение(?:\s+и\s+аудитория|/аудитория)?\s*:",
            r"\n\s*-?\s*\*\*Назначение",
            r"\n\s*Назначение(?:/аудитория)?\s*:",
            r"\n\s*Аудитория\s*:",
            r"\n\s*Теги\s*:",
            r"\.\s*Теги\s*:",
        ],
    )
    description = _extract_after_label(
        block,
        r"(?:\*\*)?Назначение(?:\s+и\s+аудитория|/аудитория)?:(?:\*\*)?\s*",
        [
            r"\.\s*(?:Спорт/активность|Спорт/дистанция|Формат забега/дистанция|Аудитория|Занятия)\s*:",
            r"\n\s*(?:-\s*)?(?:\*\*)?(?:Спорт|Аудитория|Занятия|Неопределённость|Теги)",
            r"\.\s*Теги\s*:",
        ],
    )

    sku = None if identity.lower().startswith("sku не указан") else identity
    return {
        "set_id": "race-expert-{:03d}".format(row),
        "catalog_row": row,
        "sku": sku,
        "title": title,
        "source_url": source_match.group(1),
        "price_uah": int(price_match.group(1)),
        "price_snapshot_date": SNAPSHOT_DATE,
        "composition": composition,
        "description": description,
        "tags": tags,
    }


def parse_analysis(text):
    lines = text.splitlines()
    try:
        start = next(index for index, line in enumerate(lines) if line.strip() == "## Карточки наборов") + 1
    except StopIteration:
        raise ValueError("The analysis has no 'Карточки наборов' section")

    records = []
    current = None
    for line in lines[start:]:
        parsed = _record_start(line)
        if parsed:
            if current:
                records.append(_parse_record(current[0], current[1], current[2], "\n".join(current[3])))
            row, identity, title = parsed
            current = [row, identity, title, [line]]
        elif current:
            if line.startswith("## "):
                records.append(_parse_record(current[0], current[1], current[2], "\n".join(current[3])))
                current = None
            else:
                current[3].append(line)

    if current:
        records.append(_parse_record(current[0], current[1], current[2], "\n".join(current[3])))

    rows = [record["catalog_row"] for record in records]
    if len(records) != 206:
        raise ValueError("Expected 206 in-scope sets, parsed {}".format(len(records)))
    if len(set(rows)) != len(rows):
        raise ValueError("Duplicate catalog row in the 206-set analysis")
    return records


def build_catalog(source_path=SOURCE_PATH, output_path=OUTPUT_PATH):
    text = Path(source_path).read_text(encoding="utf-8")
    records = parse_analysis(text)
    Path(output_path).write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    records = build_catalog(args.source, args.output)
    print("built {} source-linked set records at {}".format(len(records), args.output))


if __name__ == "__main__":
    main()
