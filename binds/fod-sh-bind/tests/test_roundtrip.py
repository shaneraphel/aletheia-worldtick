import json
from pathlib import Path

from fod_shs.store import FODS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    FODS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["fod_id"]
    for row in tape["rows"]:
        register(row["lmax"], fod_id=key)
    dumped = {"fod_id": key, "rows": list(FODS[key])}
    assert [row["lmax"] for row in dumped["rows"]] == [row["lmax"] for row in tape["rows"]]
