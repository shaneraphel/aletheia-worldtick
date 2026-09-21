import json
from pathlib import Path

from assembly_voice.store import CLIPS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    CLIPS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["voice_id"]
    for row in tape["rows"]:
        register(row["audio"], voice_id=key)
    dumped = {"voice_id": key, "rows": list(CLIPS[key])}
    assert [row["audio"] for row in dumped["rows"]] == [row["audio"] for row in tape["rows"]]
