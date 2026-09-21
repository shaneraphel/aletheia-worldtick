import json
from pathlib import Path

from obj_faces.store import FACES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    FACES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["obj_id"]
    for row in tape["rows"]:
        register(row["nface"], obj_id=key)
    dumped = {"obj_id": key, "rows": list(FACES[key])}
    assert [row["nface"] for row in dumped["rows"]] == [row["nface"] for row in tape["rows"]]
