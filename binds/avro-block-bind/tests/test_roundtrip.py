import json
from pathlib import Path

from avro_blocks.store import BLOCKS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    BLOCKS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["avro_id"]
    for row in tape["rows"]:
        register(row["nrec"], avro_id=key)
    dumped = {"avro_id": key, "rows": list(BLOCKS[key])}
    assert [row["nrec"] for row in dumped["rows"]] == [row["nrec"] for row in tape["rows"]]
