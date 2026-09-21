import json
from pathlib import Path

from oxts_tracks.store import FIXES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    FIXES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["oxts_id"]
    for row in tape["rows"]:
        register(row["lla"], oxts_id=key)
    dumped = {"oxts_id": key, "rows": list(FIXES[key])}
    assert [row["lla"] for row in dumped["rows"]] == [row["lla"] for row in tape["rows"]]
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    for required in schema["required"]:
        assert required in dumped
