import json
from pathlib import Path

from mcap_channels.store import CHANNELS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    CHANNELS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["mcap_id"]
    for row in tape["rows"]:
        register(row["topic"], mcap_id=key)
    dumped = {"mcap_id": key, "rows": list(CHANNELS[key])}
    assert [row["topic"] for row in dumped["rows"]] == [row["topic"] for row in tape["rows"]]
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    for required in schema["required"]:
        assert required in dumped
