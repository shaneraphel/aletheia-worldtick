import json
from pathlib import Path

from session_memory.store import MEMORY, remember

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    MEMORY.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["session_id"]
    for row in tape["rows"]:
        remember(row["text"], session_id=key)
    assert [row["text"] for row in MEMORY[key]] == [row["text"] for row in tape["rows"]]
