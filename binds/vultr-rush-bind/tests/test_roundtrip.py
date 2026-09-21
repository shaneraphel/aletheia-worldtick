import json
from pathlib import Path

from vultr_rush.store import RUNS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    RUNS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["rush_id"]
    for row in tape["rows"]:
        register(row["job"], rush_id=key)
    dumped = {"rush_id": key, "rows": list(RUNS[key])}
    assert [row["job"] for row in dumped["rows"]] == [row["job"] for row in tape["rows"]]
