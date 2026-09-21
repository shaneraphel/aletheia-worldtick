import pytest
from factory_session.store import TASKS, enqueue


def test_requires_key():
    TASKS.clear()
    with pytest.raises(ValueError):
        enqueue("job")


def test_binds_key():
    TASKS.clear()
    enqueue("a", worker_id="w-a")
    enqueue("b", worker_id="w-b")
    assert TASKS["w-a"] == ["a"]
