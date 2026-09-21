import json
from pathlib import Path

from geotiff_tiles.store import TILES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    TILES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["geotiff_id"]
    for row in tape["rows"]:
        register(row["xy"], geotiff_id=key)
    dumped = {"geotiff_id": key, "rows": list(TILES[key])}
    assert [row["xy"] for row in dumped["rows"]] == [row["xy"] for row in tape["rows"]]
