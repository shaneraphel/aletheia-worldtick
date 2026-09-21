import json
from pathlib import Path

from parquet_columns.store import COLUMNS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    COLUMNS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["parquet_id"]
    for row in tape["rows"]:
        register(row["col"], parquet_id=key)
    dumped = {"parquet_id": key, "rows": list(COLUMNS[key])}
    assert [row["col"] for row in dumped["rows"]] == [row["col"] for row in tape["rows"]]
