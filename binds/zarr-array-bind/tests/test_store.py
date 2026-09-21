import pytest
from zarr_arrays.store import ARRAYS, register


def test_requires_key():
    ARRAYS.clear()
    with pytest.raises(ValueError):
        register('temperature')


def test_binds_key():
    ARRAYS.clear()
    register('temperature', zarr_id='z-a')
    register('pressure', zarr_id='z-b')
    assert [row["name"] for row in ARRAYS["z-a"]] == ['temperature']
    assert [row["name"] for row in ARRAYS["z-b"]] == ['pressure']
