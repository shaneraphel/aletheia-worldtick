import json
from pathlib import Path

from mgz_vols.store import MGHS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    MGHS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["mgz_id"]
    for row in tape["rows"]:
        register(row["sz"], mgz_id=key)
    dumped = {"mgz_id": key, "rows": list(MGHS[key])}
    assert [row["sz"] for row in dumped["rows"]] == [row["sz"] for row in tape["rows"]]
