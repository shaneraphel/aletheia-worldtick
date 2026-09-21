import json
from pathlib import Path

from tdt_tanks.store import TANKS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    TANKS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["tdt_id"]
    for row in tape["rows"]:
        register(row["fs"], tdt_id=key)
    dumped = {"tdt_id": key, "rows": list(TANKS[key])}
    assert [row["fs"] for row in dumped["rows"]] == [row["fs"] for row in tape["rows"]]
