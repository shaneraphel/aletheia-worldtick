import json
from pathlib import Path

from bee_hives.store import HIVES, log

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    HIVES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["hive_id"]
    for row in tape["rows"]:
        log(row["note"], hive_id=key)
    dumped = {"hive_id": key, "rows": list(HIVES[key])}
    assert [row["note"] for row in dumped["rows"]] == [row["note"] for row in tape["rows"]]
