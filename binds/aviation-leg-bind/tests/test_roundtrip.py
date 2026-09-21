import json
from pathlib import Path

from aviation_legs.store import LEGS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    LEGS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["flight_id"]
    for row in tape["rows"]:
        register(row["route"], flight_id=key)
    dumped = {"flight_id": key, "rows": list(LEGS[key])}
    assert [row["route"] for row in dumped["rows"]] == [row["route"] for row in tape["rows"]]
