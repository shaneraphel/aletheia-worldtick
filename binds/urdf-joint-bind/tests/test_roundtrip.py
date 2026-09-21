import json
from pathlib import Path

from urdf_joints.store import JOINTS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    JOINTS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["urdf_id"]
    for row in tape["rows"]:
        register(row["name"], urdf_id=key)
    dumped = {"urdf_id": key, "rows": list(JOINTS[key])}
    assert [row["name"] for row in dumped["rows"]] == [row["name"] for row in tape["rows"]]
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    for required in schema["required"]:
        assert required in dumped
