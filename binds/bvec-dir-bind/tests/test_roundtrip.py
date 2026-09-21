import json
from pathlib import Path

from bvec_dirs.store import BVECS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    BVECS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["bvec_id"]
    for row in tape["rows"]:
        register(row["nd"], bvec_id=key)
    dumped = {"bvec_id": key, "rows": list(BVECS[key])}
    assert [row["nd"] for row in dumped["rows"]] == [row["nd"] for row in tape["rows"]]
