import json
from pathlib import Path

from schema_formats.store import SCHEMAS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    SCHEMAS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["schema_id"]
    for row in tape["rows"]:
        register(row["path"], schema_id=key)
    dumped = {"schema_id": key, "rows": list(SCHEMAS[key])}
    assert [row["path"] for row in dumped["rows"]] == [row["path"] for row in tape["rows"]]
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    for required in schema["required"]:
        assert required in dumped
