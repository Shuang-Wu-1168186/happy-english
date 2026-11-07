"""Build the game manifest and supplemental glossary from the existing textbook DB.

PYTHONPATH=. .venv/bin/python scripts/prepare_water_sort_data.py \
  --campaign ../happylingo-english-game/docs/campaign-200.json \
  --dictionary /tmp/happylingo-ecdict.csv --license /tmp/happylingo-ecdict-LICENSE

Only vocabulary already present in published Wordly Wise lessons is selected.
No learner or account data is exported. This does not change textbook content.
"""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re

from sqlalchemy import text

from app.core.config import Settings
from app.core.database import make_engine
from app.services.water_sort_catalog import DATA, WaterSortCatalog
from sqlalchemy.orm import Session


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--dictionary", type=Path, required=True)
    parser.add_argument("--license", type=Path, required=True)
    args = parser.parse_args()
    wanted = set()
    with make_engine(Settings().database_url).connect() as connection:
        rows = connection.execute(text(
            "SELECT l.content_json FROM learning_material_lesson l "
            "JOIN learning_material m ON m.id=l.material_id "
            "WHERE m.material_code LIKE 'wordlywise%' AND l.is_published=1 AND l.content_status='published'"
        ))
        for (raw,) in rows:
            content = json.loads(raw or "{}")
            if content.get("source", {}).get("page_kind") not in {"story-words", "word-list"}:
                continue
            for item in content.get("items", []):
                if re.match(r"^\d+\s*·", item.get("item_title", "")) and not item.get("chinese_text"):
                    wanted.add(item["english_text"].strip().casefold())
    glossary = {}
    with args.dictionary.open() as stream:
        for item in csv.DictReader(stream):
            word = item["word"].casefold()
            if word in wanted:
                # Keep the general-language definition; specialist medical/computing
                # repeats are unsuitable as a single multiple-choice option.
                lines = item["translation"].replace("\\n", "\n").splitlines()
                meaning = next((line.strip() for line in lines if line.strip() and not line.startswith("[")), "")
                if meaning:
                    glossary[word] = {"translation": meaning, "source": "ECDICT"}
    editorial = {"blasé": "厌倦享乐的；冷漠的", "métier": "专长；擅长的工作", "passé": "过时的；陈旧的",
                 "élan": "热忱；活力", "mélange": "混合物；杂烩", "habitué": "常客", "protégé": "门生；受提携者",
                 "empathize": "产生共鸣；理解他人的感受"}
    for word, meaning in editorial.items():
        if word in wanted:
            glossary[word] = {"translation": meaning, "source": "HappyLingo supplemental glossary"}
    missing = wanted - glossary.keys()
    if missing:
        raise SystemExit(f"Missing translations: {sorted(missing)}")
    DATA.mkdir(parents=True, exist_ok=True)
    data = {"source": "https://github.com/skywind3000/ECDICT", "license": "MIT",
            "dictionary_sha256": hashlib.sha256(args.dictionary.read_bytes()).hexdigest(), "words": glossary}
    (DATA / "translations.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    (DATA / "ECDICT-LICENSE.txt").write_text(args.license.read_text())
    campaign = json.loads(args.campaign.read_text())
    campaign["vocabulary_source"] = "wordly-wise-3000"
    with Session(make_engine(Settings().database_url)) as db:
        words = WaterSortCatalog(db, {"role": "admin", "id": 0}).words
    for level in campaign["levels"]:
        for bottle in level["bottles"]:
            bottle.pop("demo_word_id", None)
            slot = int(bottle["word_slot_id"].rsplit("-", 1)[1]) - 1
            bottle["word_id"] = words[slot]["word_id"]
    (DATA / "campaign-200.json").write_text(json.dumps(campaign, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"Prepared {len(campaign['levels'])} levels and {len(glossary)} supplemental definitions.")


if __name__ == "__main__":
    main()
