import json
from pathlib import Path

from alexa_intents.store import UTTERANCES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    UTTERANCES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["intent_id"]
    for row in tape["rows"]:
        register(row["text"], intent_id=key)
    dumped = {"intent_id": key, "rows": list(UTTERANCES[key])}
    assert [row["text"] for row in dumped["rows"]] == [row["text"] for row in tape["rows"]]
