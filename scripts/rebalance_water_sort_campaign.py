"""Build campaign v6: 80% random review, 20% new words after level one.

The prior v5 manifest stays untouched so existing attempts retain their fixed
word bindings.  This script only creates the manifest used by new v6 attempts.
"""

from copy import deepcopy
import json
from math import floor
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "app" / "data" / "water_sort"


def new_count(bottle_count):
    return floor(bottle_count * .2 + .5)


def rebalance(campaign):
    source = campaign["levels"]
    slot_to_word = {
        bottle["word_slot_id"]: bottle["word_id"]
        for level in source for bottle in level["bottles"]
    }
    result = deepcopy(campaign)
    introduced, next_slot = [], 0
    for level in result["levels"]:
        bottles = level["bottles"]
        fresh_count = len(bottles) if level["level"] == 1 else new_count(len(bottles))
        fresh = list(range(next_slot, next_slot + fresh_count))
        next_slot += fresh_count
        review_count = len(bottles) - fresh_count
        if review_count > len(introduced):
            raise ValueError(f"Level {level['level']} has too few prior words for review")
        rng = random.Random(level["seed"] ^ 0x52A8)
        review = rng.sample(introduced, review_count)
        assignments = [(slot, "new") for slot in fresh] + [(slot, "review") for slot in review]
        rng.shuffle(assignments)
        for bottle, (slot, role) in zip(bottles, assignments):
            slot_id = f"ww-slot-{slot + 1}"
            bottle["word_slot_id"] = slot_id
            bottle["word_id"] = slot_to_word[slot_id]
            bottle["word_role"] = role
        introduced.extend(fresh)
    return result


def main():
    source = json.loads((DATA / "campaign-200.json").read_text())
    result = rebalance(source)
    (DATA / "campaign-200-v6.json").write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n")
    new_total = sum(b["word_role"] == "new" for level in result["levels"] for b in level["bottles"])
    review_total = sum(b["word_role"] == "review" for level in result["levels"] for b in level["bottles"])
    print(f"Wrote v6 with {new_total} new and {review_total} review slots.")


if __name__ == "__main__":
    main()
