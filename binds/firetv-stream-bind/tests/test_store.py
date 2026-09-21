import pytest
from firetv_streams.store import STREAMS, queue


def test_requires_key():
    STREAMS.clear()
    with pytest.raises(ValueError):
        queue("x")


def test_binds_key():
    STREAMS.clear()
    queue("a", device_id="k-a")
    queue("b", device_id="k-b")
    assert [row["title"] for row in STREAMS["k-a"]] == ["a"]
    assert [row["title"] for row in STREAMS["k-b"]] == ["b"]
