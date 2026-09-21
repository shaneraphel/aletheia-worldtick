import json
from pathlib import Path

from agent_skills.store import SKILLS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    SKILLS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["skill_id"]
    for row in tape["rows"]:
        register(row["name"], skill_id=key)
    dumped = {"skill_id": key, "rows": list(SKILLS[key])}
    assert [row["name"] for row in dumped["rows"]] == [row["name"] for row in tape["rows"]]
