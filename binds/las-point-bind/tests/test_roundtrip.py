import json
from pathlib import Path

from las_points.store import POINTS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    POINTS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["las_id"]
    for row in tape["rows"]:
        register(row["xyz"], las_id=key)
    dumped = {"las_id": key, "rows": list(POINTS[key])}
    assert [row["xyz"] for row in dumped["rows"]] == [row["xyz"] for row in tape["rows"]]
