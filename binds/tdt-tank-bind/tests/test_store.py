import pytest
from tdt_tanks.store import TANKS, register


def test_requires_key():
    TANKS.clear()
    with pytest.raises(ValueError):
        register('24414')


def test_binds_key():
    TANKS.clear()
    register('24414', tdt_id='t-a')
    register('48828', tdt_id='t-b')
    assert [row["fs"] for row in TANKS["t-a"]] == ['24414']
    assert [row["fs"] for row in TANKS["t-b"]] == ['48828']
