import json
from pathlib import Path

from gdf_records.store import HEADERS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    HEADERS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["gdf_id"]
    for row in tape["rows"]:
        register(row["n_ch"], gdf_id=key)
    dumped = {"gdf_id": key, "rows": list(HEADERS[key])}
    assert [row["n_ch"] for row in dumped["rows"]] == [row["n_ch"] for row in tape["rows"]]
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    for required in schema["required"]:
        assert required in dumped
