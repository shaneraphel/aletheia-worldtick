import json
from pathlib import Path

from airflow_dags.store import DAGS, queue

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    DAGS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["dag_id"]
    for row in tape["rows"]:
        queue(row["op"], dag_id=key)
    dumped = {"dag_id": key, "rows": list(DAGS[key])}
    assert [row["op"] for row in dumped["rows"]] == [row["op"] for row in tape["rows"]]
