import json
from pathlib import Path

from cds_contacts.store import MESSAGES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    MESSAGES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["contact_id"]
    for row in tape["rows"]:
        register(row["text"], contact_id=key)
    dumped = {"contact_id": key, "rows": list(MESSAGES[key])}
    assert [row["text"] for row in dumped["rows"]] == [row["text"] for row in tape["rows"]]
