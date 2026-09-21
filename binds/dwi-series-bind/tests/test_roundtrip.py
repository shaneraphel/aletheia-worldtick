import json
from pathlib import Path

from dwi_series.store import DWIS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    DWIS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["dwi_id"]
    for row in tape["rows"]:
        register(row["nb0"], dwi_id=key)
    dumped = {"dwi_id": key, "rows": list(DWIS[key])}
    assert [row["nb0"] for row in dumped["rows"]] == [row["nb0"] for row in tape["rows"]]
