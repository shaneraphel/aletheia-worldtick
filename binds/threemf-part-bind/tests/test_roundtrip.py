import json
from pathlib import Path

from threemf_parts.store import PARTS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    PARTS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["threemf_id"]
    for row in tape["rows"]:
        register(row["nobj"], threemf_id=key)
    dumped = {"threemf_id": key, "rows": list(PARTS[key])}
    assert [row["nobj"] for row in dumped["rows"]] == [row["nobj"] for row in tape["rows"]]
