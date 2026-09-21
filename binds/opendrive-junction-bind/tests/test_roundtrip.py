import json
from pathlib import Path

from opendrive_junctions.store import JUNCTIONS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    JUNCTIONS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["xodr_id"]
    for row in tape["rows"]:
        register(row["rid"], xodr_id=key)
    dumped = {"xodr_id": key, "rows": list(JUNCTIONS[key])}
    assert [row["rid"] for row in dumped["rows"]] == [row["rid"] for row in tape["rows"]]
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    for required in schema["required"]:
        assert required in dumped
