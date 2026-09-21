import pytest
from nev_units.store import UNITS, register


def test_requires_key():
    UNITS.clear()
    with pytest.raises(ValueError):
        register('u1')


def test_binds_key():
    UNITS.clear()
    register('u1', nev_id='n-a')
    register('u2', nev_id='n-b')
    assert [row["uid"] for row in UNITS["n-a"]] == ['u1']
    assert [row["uid"] for row in UNITS["n-b"]] == ['u2']
