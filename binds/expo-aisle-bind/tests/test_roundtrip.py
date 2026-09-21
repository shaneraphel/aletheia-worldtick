import json
from pathlib import Path

from expo_booth.store import BOOTHS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    BOOTHS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["aisle"]
    for row in tape["rows"]:
        register(row["team"], aisle=key)
    dumped = {"aisle": key, "rows": list(BOOTHS[key])}
    assert [row["team"] for row in dumped["rows"]] == [row["team"] for row in tape["rows"]]
