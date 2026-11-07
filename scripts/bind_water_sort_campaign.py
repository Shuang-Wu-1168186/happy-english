"""Bind an exported game board to the complete published Wordly Wise catalog.

Usage from the backend checkout:
PYTHONPATH=. .venv/bin/python scripts/bind_water_sort_campaign.py \
  --campaign ../happylingo-english-game/docs/campaign-810.json \
  --output app/data/water_sort/campaign-810-v7.json
"""

import argparse
import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.database import make_engine
from app.services.water_sort_catalog import WaterSortCatalog


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    campaign = json.loads(args.campaign.read_text())
    with Session(make_engine(Settings().database_url)) as db:
        words = WaterSortCatalog(db, {"role": "admin", "id": 0}).words
    slots = [bottle for level in campaign["levels"] for bottle in level["bottles"]]
    for bottle in slots:
        bottle.pop("demo_word_id", None)
        slot = int(bottle["word_slot_id"].rsplit("-", 1)[1]) - 1
        bottle["word_id"] = words[slot]["word_id"]
    if len({b["word_id"] for b in slots if b["word_role"] == "new"}) != len(words):
        raise SystemExit("New-word bindings must cover every published textbook word exactly once.")
    campaign["vocabulary_source"] = "wordly-wise-3000"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(campaign, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"Bound {len(campaign['levels'])} levels to {len(words)} textbook words.")


if __name__ == "__main__":
    main()
