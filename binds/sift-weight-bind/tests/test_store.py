import pytest
from sift_weights.store import WEIGHTS, register


def test_requires_key():
    WEIGHTS.clear()
    with pytest.raises(ValueError):
        register(1)


def test_binds_key():
    WEIGHTS.clear()
    register(1, sift_id='s-a')
    register(2, sift_id='s-b')
    assert [row["mu"] for row in WEIGHTS["s-a"]] == [1]
    assert [row["mu"] for row in WEIGHTS["s-b"]] == [2]
