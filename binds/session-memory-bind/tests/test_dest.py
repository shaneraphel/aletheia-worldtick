import pytest
from session_memory.store import MEMORY, remember


def test_requires_key():
    MEMORY.clear()
    with pytest.raises(ValueError):
        remember("x")


def test_binds_key():
    MEMORY.clear()
    remember("a", session_id="s-a")
    remember("b", session_id="s-b")
    assert [row["text"] for row in MEMORY["s-a"]] == ["a"]
