import pytest
from ring_chimes.store import CHIMES, ring


def test_requires_key():
    CHIMES.clear()
    with pytest.raises(ValueError):
        ring("x")


def test_binds_key():
    CHIMES.clear()
    ring("a", doorbell_id="k-a")
    ring("b", doorbell_id="k-b")
    assert [row["event"] for row in CHIMES["k-a"]] == ["a"]
    assert [row["event"] for row in CHIMES["k-b"]] == ["b"]
