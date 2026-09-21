import pytest
from band_agents.store import AGENTS, register


def test_requires_key():
    AGENTS.clear()
    with pytest.raises(ValueError):
        register("goal-a")


def test_binds_key():
    AGENTS.clear()
    register("goal-a", band_id="d-a")
    register("goal-b", band_id="d-b")
    assert [row["goal"] for row in AGENTS["d-a"]] == ["goal-a"]
    assert [row["goal"] for row in AGENTS["d-b"]] == ["goal-b"]
