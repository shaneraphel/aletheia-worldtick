import pytest
from agent_skills.store import SKILLS, register


def test_requires_key():
    SKILLS.clear()
    with pytest.raises(ValueError):
        register("x")


def test_binds_key():
    SKILLS.clear()
    register("a", skill_id="k-a")
    register("b", skill_id="k-b")
    assert [row["name"] for row in SKILLS["k-a"]] == ["a"]
    assert [row["name"] for row in SKILLS["k-b"]] == ["b"]
