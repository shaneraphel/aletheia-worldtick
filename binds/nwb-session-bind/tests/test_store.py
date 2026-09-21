import pytest
from nwb_sessions.store import SESSIONS, register


def test_requires_key():
    SESSIONS.clear()
    with pytest.raises(ValueError):
        register('sub-a.nwb')


def test_binds_key():
    SESSIONS.clear()
    register('sub-a.nwb', nwb_id='n-a')
    register('sub-b.nwb', nwb_id='n-b')
    assert [row["path"] for row in SESSIONS["n-a"]] == ['sub-a.nwb']
    assert [row["path"] for row in SESSIONS["n-b"]] == ['sub-b.nwb']
