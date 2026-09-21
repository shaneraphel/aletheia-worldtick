import json
from pathlib import Path

from ply_meshes.store import FACES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    FACES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["ply_id"]
    for row in tape["rows"]:
        register(row["n"], ply_id=key)
    dumped = {"ply_id": key, "rows": list(FACES[key])}
    assert [row["n"] for row in dumped["rows"]] == [row["n"] for row in tape["rows"]]
