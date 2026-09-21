import json
from pathlib import Path

from pcd_clouds.store import CLOUDS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    CLOUDS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["pcd_id"]
    for row in tape["rows"]:
        register(row["path"], pcd_id=key)
    dumped = {"pcd_id": key, "rows": list(CLOUDS[key])}
    assert [row["path"] for row in dumped["rows"]] == [row["path"] for row in tape["rows"]]
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    for required in schema["required"]:
        assert required in dumped
