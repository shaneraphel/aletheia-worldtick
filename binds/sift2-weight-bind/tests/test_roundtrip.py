import json
from pathlib import Path

from sift2_weights.store import STREAM_W, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    STREAM_W.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["sift2_id"]
    for row in tape["rows"]:
        register(row["sift2"], sift2_id=key)
    dumped = {"sift2_id": key, "rows": list(STREAM_W[key])}
    assert [row["sift2"] for row in dumped["rows"]] == [row["sift2"] for row in tape["rows"]]
