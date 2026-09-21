import json
from pathlib import Path

from peak_dirs.store import PEAKS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    PEAKS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["peak_id"]
    for row in tape["rows"]:
        register(row["npeak"], peak_id=key)
    dumped = {"peak_id": key, "rows": list(PEAKS[key])}
    assert [row["npeak"] for row in dumped["rows"]] == [row["npeak"] for row in tape["rows"]]
