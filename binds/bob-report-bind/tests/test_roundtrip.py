import json
from pathlib import Path

from bob_reports.store import REPORTS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    REPORTS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["bob_id"]
    for row in tape["rows"]:
        register(row["note"], bob_id=key)
    dumped = {"bob_id": key, "rows": list(REPORTS[key])}
    assert [row["note"] for row in dumped["rows"]] == [row["note"] for row in tape["rows"]]
