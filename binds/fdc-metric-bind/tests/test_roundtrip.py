import json
from pathlib import Path

from fdc_metrics.store import FDCS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    FDCS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["fdc_id"]
    for row in tape["rows"]:
        register(row["fdc"], fdc_id=key)
    dumped = {"fdc_id": key, "rows": list(FDCS[key])}
    assert [row["fdc"] for row in dumped["rows"]] == [row["fdc"] for row in tape["rows"]]
