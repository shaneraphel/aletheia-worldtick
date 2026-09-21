import json
from pathlib import Path

from cifti_maps.store import MAPS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    MAPS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["cifti_id"]
    for row in tape["rows"]:
        register(row["dconn"], cifti_id=key)
    dumped = {"cifti_id": key, "rows": list(MAPS[key])}
    assert [row["dconn"] for row in dumped["rows"]] == [row["dconn"] for row in tape["rows"]]
