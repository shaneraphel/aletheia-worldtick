import pytest
from netcdf_vars.store import VARS, register


def test_requires_key():
    VARS.clear()
    with pytest.raises(ValueError):
        register('temperature')


def test_binds_key():
    VARS.clear()
    register('temperature', netcdf_id='n-a')
    register('salinity', netcdf_id='n-b')
    assert [row["var"] for row in VARS["n-a"]] == ['temperature']
    assert [row["var"] for row in VARS["n-b"]] == ['salinity']
