import json
from pathlib import Path

from mjcf_bodies.store import BODIES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    BODIES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["mjcf_id"]
    for row in tape["rows"]:
        register(row["link"], mjcf_id=key)
    dumped = {"mjcf_id": key, "rows": list(BODIES[key])}
    assert [row["link"] for row in dumped["rows"]] == [row["link"] for row in tape["rows"]]
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    for required in schema["required"]:
        assert required in dumped
