import json
from pathlib import Path

from sift_weights.store import WEIGHTS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    WEIGHTS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["sift_id"]
    for row in tape["rows"]:
        register(row["mu"], sift_id=key)
    dumped = {"sift_id": key, "rows": list(WEIGHTS[key])}
    assert [row["mu"] for row in dumped["rows"]] == [row["mu"] for row in tape["rows"]]
