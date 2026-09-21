import pytest
from urdf_joints.store import JOINTS, register


def test_requires_key():
    JOINTS.clear()
    with pytest.raises(ValueError):
        register('shoulder')


def test_binds_key():
    JOINTS.clear()
    register('shoulder', urdf_id='u-a')
    register('elbow', urdf_id='u-b')
    assert [row["name"] for row in JOINTS["u-a"]] == ['shoulder']
    assert [row["name"] for row in JOINTS["u-b"]] == ['elbow']
