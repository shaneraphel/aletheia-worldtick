import json
from pathlib import Path

from orc_stripes.store import STRIPES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    STRIPES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["orc_id"]
    for row in tape["rows"]:
        register(row["rid"], orc_id=key)
    dumped = {"orc_id": key, "rows": list(STRIPES[key])}
    assert [row["rid"] for row in dumped["rows"]] == [row["rid"] for row in tape["rows"]]
