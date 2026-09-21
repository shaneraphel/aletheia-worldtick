import json
from pathlib import Path

from iceberg_snapshots.store import SNAPSHOTS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    SNAPSHOTS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["iceberg_id"]
    for row in tape["rows"]:
        register(row["sid"], iceberg_id=key)
    dumped = {"iceberg_id": key, "rows": list(SNAPSHOTS[key])}
    assert [row["sid"] for row in dumped["rows"]] == [row["sid"] for row in tape["rows"]]
