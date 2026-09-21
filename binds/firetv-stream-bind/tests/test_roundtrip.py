import json
from pathlib import Path

from firetv_streams.store import STREAMS, queue

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    STREAMS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["device_id"]
    for row in tape["rows"]:
        queue(row["title"], device_id=key)
    dumped = {"device_id": key, "rows": list(STREAMS[key])}
    assert [row["title"] for row in dumped["rows"]] == [row["title"] for row in tape["rows"]]
