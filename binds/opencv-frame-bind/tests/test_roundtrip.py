import json
from pathlib import Path

from opencv_frames.store import FRAMES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    FRAMES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["camera_id"]
    for row in tape["rows"]:
        register(row["frame"], camera_id=key)
    dumped = {"camera_id": key, "rows": list(FRAMES[key])}
    assert [row["frame"] for row in dumped["rows"]] == [row["frame"] for row in tape["rows"]]
