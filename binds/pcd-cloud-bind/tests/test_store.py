import pytest
from pcd_clouds.store import CLOUDS, register


def test_requires_key():
    CLOUDS.clear()
    with pytest.raises(ValueError):
        register('cloud.pcd')


def test_binds_key():
    CLOUDS.clear()
    register('cloud.pcd', pcd_id='p-a')
    register('scan.pcd', pcd_id='p-b')
    assert [row["path"] for row in CLOUDS["p-a"]] == ['cloud.pcd']
    assert [row["path"] for row in CLOUDS["p-b"]] == ['scan.pcd']
