import pytest
from nrrd_axes.store import AXES, register


def test_requires_key():
    AXES.clear()
    with pytest.raises(ValueError):
        register('1.0')


def test_binds_key():
    AXES.clear()
    register('1.0', nrrd_id='r-a')
    register('2.0', nrrd_id='r-b')
    assert [row["spc"] for row in AXES["r-a"]] == ['1.0']
    assert [row["spc"] for row in AXES["r-b"]] == ['2.0']
