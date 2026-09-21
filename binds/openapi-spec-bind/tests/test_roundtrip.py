import json
from pathlib import Path

from openapi_specs.store import SPECS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    SPECS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["openapi_id"]
    for row in tape["rows"]:
        register(row["href"], openapi_id=key)
    dumped = {"openapi_id": key, "rows": list(SPECS[key])}
    assert [row["href"] for row in dumped["rows"]] == [row["href"] for row in tape["rows"]]
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    for required in schema["required"]:
        assert required in dumped
