import json
from pathlib import Path

from agentweek_slots.store import SLOTS, book

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    SLOTS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["week_id"]
    for row in tape["rows"]:
        book(row["agent"], week_id=key)
    dumped = {"week_id": key, "rows": list(SLOTS[key])}
    assert [row["agent"] for row in dumped["rows"]] == [row["agent"] for row in tape["rows"]]
