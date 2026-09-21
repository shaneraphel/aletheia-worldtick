import json
from pathlib import Path

from fib_vols.store import FIBS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    FIBS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["fib_id"]
    for row in tape["rows"]:
        register(row["nfd"], fib_id=key)
    dumped = {"fib_id": key, "rows": list(FIBS[key])}
    assert [row["nfd"] for row in dumped["rows"]] == [row["nfd"] for row in tape["rows"]]
