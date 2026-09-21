import json
from pathlib import Path

from minc_slices.store import SLICES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    SLICES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["minc_id"]
    for row in tape["rows"]:
        register(row["z"], minc_id=key)
    dumped = {"minc_id": key, "rows": list(SLICES[key])}
    assert [row["z"] for row in dumped["rows"]] == [row["z"] for row in tape["rows"]]
