import json
from pathlib import Path

from afd_dens.store import DENS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    DENS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["afd_id"]
    for row in tape["rows"]:
        register(row["afd"], afd_id=key)
    dumped = {"afd_id": key, "rows": list(DENS[key])}
    assert [row["afd"] for row in dumped["rows"]] == [row["afd"] for row in tape["rows"]]
