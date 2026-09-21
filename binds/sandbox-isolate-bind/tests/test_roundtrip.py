import json
from pathlib import Path

from sandbox_jobs.store import JOBS, enqueue

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    JOBS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["isolate_id"]
    for row in tape["rows"]:
        enqueue(row["cmd"], isolate_id=key)
    dumped = {"isolate_id": key, "rows": list(JOBS[key])}
    assert [row["cmd"] for row in dumped["rows"]] == [row["cmd"] for row in tape["rows"]]
