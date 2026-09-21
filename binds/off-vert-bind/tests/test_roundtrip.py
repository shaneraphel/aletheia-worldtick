import json
from pathlib import Path

from off_verts.store import VERTS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    VERTS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["off_id"]
    for row in tape["rows"]:
        register(row["nv"], off_id=key)
    dumped = {"off_id": key, "rows": list(VERTS[key])}
    assert [row["nv"] for row in dumped["rows"]] == [row["nv"] for row in tape["rows"]]
