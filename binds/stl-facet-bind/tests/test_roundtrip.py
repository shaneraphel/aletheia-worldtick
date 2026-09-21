import json
from pathlib import Path

from stl_facets.store import FACETS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    FACETS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["stl_id"]
    for row in tape["rows"]:
        register(row["ntri"], stl_id=key)
    dumped = {"stl_id": key, "rows": list(FACETS[key])}
    assert [row["ntri"] for row in dumped["rows"]] == [row["ntri"] for row in tape["rows"]]
