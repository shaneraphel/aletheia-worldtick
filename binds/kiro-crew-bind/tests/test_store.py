import pytest
from kiro_crew.store import CREWS, register


def test_requires_key():
    CREWS.clear()
    with pytest.raises(ValueError):
        register("task-a")


def test_binds_key():
    CREWS.clear()
    register("task-a", kiro_id="k-a")
    register("task-b", kiro_id="k-b")
    assert [row["task"] for row in CREWS["k-a"]] == ["task-a"]
    assert [row["task"] for row in CREWS["k-b"]] == ["task-b"]
