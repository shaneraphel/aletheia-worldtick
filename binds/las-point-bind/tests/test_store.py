import pytest
from las_points.store import POINTS, register


def test_requires_key():
    POINTS.clear()
    with pytest.raises(ValueError):
        register('0,0,0')


def test_binds_key():
    POINTS.clear()
    register('0,0,0', las_id='l-a')
    register('1,1,1', las_id='l-b')
    assert [row["xyz"] for row in POINTS["l-a"]] == ['0,0,0']
    assert [row["xyz"] for row in POINTS["l-b"]] == ['1,1,1']
