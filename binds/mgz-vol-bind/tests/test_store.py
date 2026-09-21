import pytest
from mgz_vols.store import MGHS, register


def test_requires_key():
    MGHS.clear()
    with pytest.raises(ValueError):
        register('256')


def test_binds_key():
    MGHS.clear()
    register('256', mgz_id='m-a')
    register('128', mgz_id='m-b')
    assert [row["sz"] for row in MGHS["m-a"]] == ['256']
    assert [row["sz"] for row in MGHS["m-b"]] == ['128']
