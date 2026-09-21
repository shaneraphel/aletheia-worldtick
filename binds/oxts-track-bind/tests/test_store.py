import pytest
from oxts_tracks.store import FIXES, register


def test_requires_key():
    FIXES.clear()
    with pytest.raises(ValueError):
        register('49.0,8.4')


def test_binds_key():
    FIXES.clear()
    register('49.0,8.4', oxts_id='x-a')
    register('49.1,8.5', oxts_id='x-b')
    assert [row["lla"] for row in FIXES["x-a"]] == ['49.0,8.4']
    assert [row["lla"] for row in FIXES["x-b"]] == ['49.1,8.5']
