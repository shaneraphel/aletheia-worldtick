import json
from pathlib import Path

from gltf_meshes.store import MESHES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    MESHES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["gltf_id"]
    for row in tape["rows"]:
        register(row["prim"], gltf_id=key)
    dumped = {"gltf_id": key, "rows": list(MESHES[key])}
    assert [row["prim"] for row in dumped["rows"]] == [row["prim"] for row in tape["rows"]]
