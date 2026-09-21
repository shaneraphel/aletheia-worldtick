import json
from pathlib import Path

from hdf5_groups.store import GROUPS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    GROUPS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["hdf5_id"]
    for row in tape["rows"]:
        register(row["path"], hdf5_id=key)
    dumped = {"hdf5_id": key, "rows": list(GROUPS[key])}
    assert [row["path"] for row in dumped["rows"]] == [row["path"] for row in tape["rows"]]
