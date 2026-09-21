import json
from pathlib import Path

from ring_chimes.store import CHIMES, ring

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    CHIMES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["doorbell_id"]
    for row in tape["rows"]:
        ring(row["event"], doorbell_id=key)
    dumped = {"doorbell_id": key, "rows": list(CHIMES[key])}
    assert [row["event"] for row in dumped["rows"]] == [row["event"] for row in tape["rows"]]
