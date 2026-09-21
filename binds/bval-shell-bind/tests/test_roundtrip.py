import json
from pathlib import Path

from bval_shells.store import BVALS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    BVALS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["bval_id"]
    for row in tape["rows"]:
        register(row["nb"], bval_id=key)
    dumped = {"bval_id": key, "rows": list(BVALS[key])}
    assert [row["nb"] for row in dumped["rows"]] == [row["nb"] for row in tape["rows"]]
