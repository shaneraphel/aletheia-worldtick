import json
from pathlib import Path

from opencv_cool.store import PIXELS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    PIXELS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["graviton_id"]
    for row in tape["rows"]:
        register(row["tile"], graviton_id=key)
    dumped = {"graviton_id": key, "rows": list(PIXELS[key])}
    assert [row["tile"] for row in dumped["rows"]] == [row["tile"] for row in tape["rows"]]
