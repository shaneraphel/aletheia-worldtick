import json
from pathlib import Path

from airflow_hitl.store import APPROVALS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    APPROVALS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["hitl_id"]
    for row in tape["rows"]:
        register(row["op"], hitl_id=key)
    dumped = {"hitl_id": key, "rows": list(APPROVALS[key])}
    assert [row["op"] for row in dumped["rows"]] == [row["op"] for row in tape["rows"]]
