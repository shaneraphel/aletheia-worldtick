import pytest
from sift2_weights.store import STREAM_W, register


def test_requires_key():
    STREAM_W.clear()
    with pytest.raises(ValueError):
        register(1)


def test_binds_key():
    STREAM_W.clear()
    register(1, sift2_id='s2-a')
    register(2, sift2_id='s2-b')
    assert [row["sift2"] for row in STREAM_W["s2-a"]] == [1]
    assert [row["sift2"] for row in STREAM_W["s2-b"]] == [2]
