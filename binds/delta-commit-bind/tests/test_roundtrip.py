import json
from pathlib import Path

from delta_commits.store import COMMITS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    COMMITS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["delta_id"]
    for row in tape["rows"]:
        register(row["ver"], delta_id=key)
    dumped = {"delta_id": key, "rows": list(COMMITS[key])}
    assert [row["ver"] for row in dumped["rows"]] == [row["ver"] for row in tape["rows"]]
