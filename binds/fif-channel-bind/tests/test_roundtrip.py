import json
from pathlib import Path

from fif_channels.store import CHANNELS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    CHANNELS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["fif_id"]
    for row in tape["rows"]:
        register(row["ch"], fif_id=key)
    dumped = {"fif_id": key, "rows": list(CHANNELS[key])}
    assert [row["ch"] for row in dumped["rows"]] == [row["ch"] for row in tape["rows"]]
