import json
from pathlib import Path

from resource_tapes.store import TAPES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    TAPES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["tape_id"]
    for row in tape["rows"]:
        register(row["uri"], tape_id=key)
    dumped = {"tape_id": key, "rows": list(TAPES[key])}
    assert [row["uri"] for row in dumped["rows"]] == [row["uri"] for row in tape["rows"]]
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    for required in schema["required"]:
        assert required in dumped
