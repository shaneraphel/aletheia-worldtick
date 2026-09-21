import json
from pathlib import Path

from nsx_chans.store import CHANS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    CHANS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["nsx_id"]
    for row in tape["rows"]:
        register(row["sr"], nsx_id=key)
    dumped = {"nsx_id": key, "rows": list(CHANS[key])}
    assert [row["sr"] for row in dumped["rows"]] == [row["sr"] for row in tape["rows"]]
