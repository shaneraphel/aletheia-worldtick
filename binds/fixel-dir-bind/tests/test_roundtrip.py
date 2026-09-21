import json
from pathlib import Path

from fixel_dirs.store import FIXELS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    FIXELS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["fixel_id"]
    for row in tape["rows"]:
        register(row["ndir"], fixel_id=key)
    dumped = {"fixel_id": key, "rows": list(FIXELS[key])}
    assert [row["ndir"] for row in dumped["rows"]] == [row["ndir"] for row in tape["rows"]]
