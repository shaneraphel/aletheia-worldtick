import json
from pathlib import Path

from afq_bundles.store import BUNDLES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    BUNDLES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["afq_id"]
    for row in tape["rows"]:
        register(row["ntr"], afq_id=key)
    dumped = {"afq_id": key, "rows": list(BUNDLES[key])}
    assert [row["ntr"] for row in dumped["rows"]] == [row["ntr"] for row in tape["rows"]]
