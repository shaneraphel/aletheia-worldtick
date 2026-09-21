import json
from pathlib import Path

from netcdf_vars.store import VARS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    VARS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["netcdf_id"]
    for row in tape["rows"]:
        register(row["var"], netcdf_id=key)
    dumped = {"netcdf_id": key, "rows": list(VARS[key])}
    assert [row["var"] for row in dumped["rows"]] == [row["var"] for row in tape["rows"]]
