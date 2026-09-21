import json
from pathlib import Path

from geoparquet_features.store import FEATURES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    FEATURES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["geoparquet_id"]
    for row in tape["rows"]:
        register(row["geom"], geoparquet_id=key)
    dumped = {"geoparquet_id": key, "rows": list(FEATURES[key])}
    assert [row["geom"] for row in dumped["rows"]] == [row["geom"] for row in tape["rows"]]
