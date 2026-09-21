import json
from pathlib import Path

from trx_groups.store import GROUPS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    GROUPS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["trx_id"]
    for row in tape["rows"]:
        register(row["ng"], trx_id=key)
    dumped = {"trx_id": key, "rows": list(GROUPS[key])}
    assert [row["ng"] for row in dumped["rows"]] == [row["ng"] for row in tape["rows"]]
