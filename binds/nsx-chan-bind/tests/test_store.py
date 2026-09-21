import pytest
from nsx_chans.store import CHANS, register


def test_requires_key():
    CHANS.clear()
    with pytest.raises(ValueError):
        register('30000')


def test_binds_key():
    CHANS.clear()
    register('30000', nsx_id='x-a')
    register('10000', nsx_id='x-b')
    assert [row["sr"] for row in CHANS["x-a"]] == ['30000']
    assert [row["sr"] for row in CHANS["x-b"]] == ['10000']
