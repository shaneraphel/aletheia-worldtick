import pytest
from gltf_meshes.store import MESHES, register


def test_requires_key():
    MESHES.clear()
    with pytest.raises(ValueError):
        register(3)


def test_binds_key():
    MESHES.clear()
    register(3, gltf_id='g-a')
    register(9, gltf_id='g-b')
    assert [row["prim"] for row in MESHES["g-a"]] == [3]
    assert [row["prim"] for row in MESHES["g-b"]] == [9]
