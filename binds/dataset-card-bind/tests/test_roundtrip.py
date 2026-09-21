import json
from pathlib import Path

from dataset_cards.store import CARDS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    CARDS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["card_id"]
    for row in tape["rows"]:
        register(row["doi"], card_id=key)
    dumped = {"card_id": key, "rows": list(CARDS[key])}
    assert [row["doi"] for row in dumped["rows"]] == [row["doi"] for row in tape["rows"]]
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    for required in schema["required"]:
        assert required in dumped
