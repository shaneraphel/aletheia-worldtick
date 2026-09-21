import json
from pathlib import Path

from edf_signals.store import SIGNALS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    SIGNALS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["edf_id"]
    for row in tape["rows"]:
        register(row["label"], edf_id=key)
    dumped = {"edf_id": key, "rows": list(SIGNALS[key])}
    assert [row["label"] for row in dumped["rows"]] == [row["label"] for row in tape["rows"]]
