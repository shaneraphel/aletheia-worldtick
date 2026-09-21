import json
from pathlib import Path

from factory_session.store import TASKS, enqueue

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    TASKS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["worker_id"]
    for row in tape["rows"]:
        enqueue(row["job"], worker_id=key)
    dumped = list(TASKS[key])
    assert dumped == [row["job"] for row in tape["rows"]]
