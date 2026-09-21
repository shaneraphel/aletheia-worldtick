import json
from pathlib import Path

from gifti_surfs.store import SURFS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    SURFS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["gifti_id"]
    for row in tape["rows"]:
        register(row["nvert"], gifti_id=key)
    dumped = {"gifti_id": key, "rows": list(SURFS[key])}
    assert [row["nvert"] for row in dumped["rows"]] == [row["nvert"] for row in tape["rows"]]
