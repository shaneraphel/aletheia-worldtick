import json
from pathlib import Path

from trk_streams.store import STREAMS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    STREAMS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["trk_id"]
    for row in tape["rows"]:
        register(row["npts"], trk_id=key)
    dumped = {"trk_id": key, "rows": list(STREAMS[key])}
    assert [row["npts"] for row in dumped["rows"]] == [row["npts"] for row in tape["rows"]]
