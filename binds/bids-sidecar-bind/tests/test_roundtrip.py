import json
from pathlib import Path

from bids_sidecars.store import SIDECARS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    SIDECARS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["bids_id"]
    for row in tape["rows"]:
        register(row["suffix"], bids_id=key)
    dumped = {"bids_id": key, "rows": list(SIDECARS[key])}
    assert [row["suffix"] for row in dumped["rows"]] == [row["suffix"] for row in tape["rows"]]
