import json
from pathlib import Path

from zarr_arrays.store import ARRAYS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    ARRAYS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["zarr_id"]
    for row in tape["rows"]:
        register(row["name"], zarr_id=key)
    dumped = {"zarr_id": key, "rows": list(ARRAYS[key])}
    assert [row["name"] for row in dumped["rows"]] == [row["name"] for row in tape["rows"]]
