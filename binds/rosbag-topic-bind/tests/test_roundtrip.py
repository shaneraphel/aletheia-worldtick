import json
from pathlib import Path

from rosbag_topics.store import TOPICS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    TOPICS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["bag_id"]
    for row in tape["rows"]:
        register(row["name"], bag_id=key)
    dumped = {"bag_id": key, "rows": list(TOPICS[key])}
    assert [row["name"] for row in dumped["rows"]] == [row["name"] for row in tape["rows"]]
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    for required in schema["required"]:
        assert required in dumped
