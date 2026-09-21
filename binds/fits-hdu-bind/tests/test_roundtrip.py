import json
from pathlib import Path

from fits_hdus.store import HDUS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    HDUS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["fits_id"]
    for row in tape["rows"]:
        register(row["ext"], fits_id=key)
    dumped = {"fits_id": key, "rows": list(HDUS[key])}
    assert [row["ext"] for row in dumped["rows"]] == [row["ext"] for row in tape["rows"]]
