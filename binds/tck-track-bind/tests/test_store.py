import pytest
from tck_tracks.store import TRACKS, register


def test_requires_key():
    TRACKS.clear()
    with pytest.raises(ValueError):
        register(25)


def test_binds_key():
    TRACKS.clear()
    register(25, tck_id='c-a')
    register(50, tck_id='c-b')
    assert [row["nsl"] for row in TRACKS["c-a"]] == [25]
    assert [row["nsl"] for row in TRACKS["c-b"]] == [50]
