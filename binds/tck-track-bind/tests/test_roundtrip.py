import json
from pathlib import Path

from tck_tracks.store import TRACKS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    TRACKS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["tck_id"]
    for row in tape["rows"]:
        register(row["nsl"], tck_id=key)
    dumped = {"tck_id": key, "rows": list(TRACKS[key])}
    assert [row["nsl"] for row in dumped["rows"]] == [row["nsl"] for row in tape["rows"]]
