import json
from pathlib import Path

from opencv_vision.store import ACTIONS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    ACTIONS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["vision_id"]
    for row in tape["rows"]:
        register(row["act"], vision_id=key)
    dumped = {"vision_id": key, "rows": list(ACTIONS[key])}
    assert [row["act"] for row in dumped["rows"]] == [row["act"] for row in tape["rows"]]
