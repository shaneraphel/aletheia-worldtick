import json
from pathlib import Path

from arrow_batches.store import BATCHES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    BATCHES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["arrow_id"]
    for row in tape["rows"]:
        register(row["ncols"], arrow_id=key)
    dumped = {"arrow_id": key, "rows": list(BATCHES[key])}
    assert [row["ncols"] for row in dumped["rows"]] == [row["ncols"] for row in tape["rows"]]
