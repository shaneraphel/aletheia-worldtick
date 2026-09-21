import pytest
from resource_tapes.store import TAPES, register


def test_requires_key():
    TAPES.clear()
    with pytest.raises(ValueError):
        register('edf://a')


def test_binds_key():
    TAPES.clear()
    register('edf://a', tape_id='t-a')
    register('wfdb://b', tape_id='t-b')
    assert [row["uri"] for row in TAPES["t-a"]] == ["edf://a"]
    assert [row["uri"] for row in TAPES["t-b"]] == ["wfdb://b"]
