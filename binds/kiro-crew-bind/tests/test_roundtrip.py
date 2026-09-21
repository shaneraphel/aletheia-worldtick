import json
from pathlib import Path

from kiro_crew.store import CREWS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    CREWS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["kiro_id"]
    for row in tape["rows"]:
        register(row["task"], kiro_id=key)
    dumped = {"kiro_id": key, "rows": list(CREWS[key])}
    assert [row["task"] for row in dumped["rows"]] == [row["task"] for row in tape["rows"]]
