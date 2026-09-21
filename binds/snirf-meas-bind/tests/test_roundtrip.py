import json
from pathlib import Path

from snirf_meas.store import MEAS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    MEAS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["snirf_id"]
    for row in tape["rows"]:
        register(row["wl"], snirf_id=key)
    dumped = {"snirf_id": key, "rows": list(MEAS[key])}
    assert [row["wl"] for row in dumped["rows"]] == [row["wl"] for row in tape["rows"]]
