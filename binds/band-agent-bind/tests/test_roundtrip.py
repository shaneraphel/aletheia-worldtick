import json
from pathlib import Path

from band_agents.store import AGENTS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    AGENTS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["band_id"]
    for row in tape["rows"]:
        register(row["goal"], band_id=key)
    dumped = {"band_id": key, "rows": list(AGENTS[key])}
    assert [row["goal"] for row in dumped["rows"]] == [row["goal"] for row in tape["rows"]]
