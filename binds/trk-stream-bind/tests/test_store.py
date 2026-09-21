import pytest
from trk_streams.store import STREAMS, register


def test_requires_key():
    STREAMS.clear()
    with pytest.raises(ValueError):
        register(40)


def test_binds_key():
    STREAMS.clear()
    register(40, trk_id='k-a')
    register(80, trk_id='k-b')
    assert [row["npts"] for row in STREAMS["k-a"]] == [40]
    assert [row["npts"] for row in STREAMS["k-b"]] == [80]
