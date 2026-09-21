import json
from pathlib import Path

from rosbag2_messages.store import MESSAGES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    MESSAGES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["bag2_id"]
    for row in tape["rows"]:
        register(row["typ"], bag2_id=key)
    dumped = {"bag2_id": key, "rows": list(MESSAGES[key])}
    assert [row["typ"] for row in dumped["rows"]] == [row["typ"] for row in tape["rows"]]
