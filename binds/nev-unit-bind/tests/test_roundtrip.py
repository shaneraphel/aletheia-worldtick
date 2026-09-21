import json
from pathlib import Path

from nev_units.store import UNITS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    UNITS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["nev_id"]
    for row in tape["rows"]:
        register(row["uid"], nev_id=key)
    dumped = {"nev_id": key, "rows": list(UNITS[key])}
    assert [row["uid"] for row in dumped["rows"]] == [row["uid"] for row in tape["rows"]]
