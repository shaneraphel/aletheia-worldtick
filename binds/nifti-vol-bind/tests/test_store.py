import pytest
from nifti_vols.store import VOLS, register


def test_requires_key():
    VOLS.clear()
    with pytest.raises(ValueError):
        register('64')


def test_binds_key():
    VOLS.clear()
    register('64', nifti_id='v-a')
    register('128', nifti_id='v-b')
    assert [row["dim"] for row in VOLS["v-a"]] == ['64']
    assert [row["dim"] for row in VOLS["v-b"]] == ['128']
