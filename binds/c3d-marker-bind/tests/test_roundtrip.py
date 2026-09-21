import json
from pathlib import Path

from c3d_markers.store import MARKERS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    MARKERS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["c3d_id"]
    for row in tape["rows"]:
        register(row["lab"], c3d_id=key)
    dumped = {"c3d_id": key, "rows": list(MARKERS[key])}
    assert [row["lab"] for row in dumped["rows"]] == [row["lab"] for row in tape["rows"]]
