import json
from pathlib import Path

from airflow_llm.store import BRANCHES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    BRANCHES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["llm_id"]
    for row in tape["rows"]:
        register(row["prompt"], llm_id=key)
    dumped = {"llm_id": key, "rows": list(BRANCHES[key])}
    assert [row["prompt"] for row in dumped["rows"]] == [row["prompt"] for row in tape["rows"]]
