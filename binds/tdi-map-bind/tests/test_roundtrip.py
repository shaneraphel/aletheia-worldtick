import json
from pathlib import Path

from tdi_maps.store import MAPS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    MAPS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["tdi_id"]
    for row in tape["rows"]:
        register(row["tdi"], tdi_id=key)
    dumped = {"tdi_id": key, "rows": list(MAPS[key])}
    assert [row["tdi"] for row in dumped["rows"]] == [row["tdi"] for row in tape["rows"]]
