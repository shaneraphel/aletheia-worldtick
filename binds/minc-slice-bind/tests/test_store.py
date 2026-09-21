import pytest
from minc_slices.store import SLICES, register


def test_requires_key():
    SLICES.clear()
    with pytest.raises(ValueError):
        register('0')


def test_binds_key():
    SLICES.clear()
    register('0', minc_id='m-a')
    register('1', minc_id='m-b')
    assert [row["z"] for row in SLICES["m-a"]] == ['0']
    assert [row["z"] for row in SLICES["m-b"]] == ['1']
