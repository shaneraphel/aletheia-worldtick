import json
from pathlib import Path

from nwb_sessions.store import SESSIONS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    SESSIONS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["nwb_id"]
    for row in tape["rows"]:
        register(row["path"], nwb_id=key)
    dumped = {"nwb_id": key, "rows": list(SESSIONS[key])}
    assert [row["path"] for row in dumped["rows"]] == [row["path"] for row in tape["rows"]]
