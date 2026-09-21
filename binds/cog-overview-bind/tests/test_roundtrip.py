import json
from pathlib import Path

from cog_overviews.store import OVERVIEWS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    OVERVIEWS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["cog_id"]
    for row in tape["rows"]:
        register(row["lvl"], cog_id=key)
    dumped = {"cog_id": key, "rows": list(OVERVIEWS[key])}
    assert [row["lvl"] for row in dumped["rows"]] == [row["lvl"] for row in tape["rows"]]
