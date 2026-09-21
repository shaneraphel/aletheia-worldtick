import pytest
from agentweek_slots.store import SLOTS, book


def test_requires_key():
    SLOTS.clear()
    with pytest.raises(ValueError):
        book("x")


def test_binds_key():
    SLOTS.clear()
    book("a", week_id="k-a")
    book("b", week_id="k-b")
    assert [row["agent"] for row in SLOTS["k-a"]] == ["a"]
    assert [row["agent"] for row in SLOTS["k-b"]] == ["b"]
