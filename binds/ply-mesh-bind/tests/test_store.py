import pytest
from ply_meshes.store import FACES, register


def test_requires_key():
    FACES.clear()
    with pytest.raises(ValueError):
        register(3)


def test_binds_key():
    FACES.clear()
    register(3, ply_id='p-a')
    register(4, ply_id='p-b')
    assert [row["n"] for row in FACES["p-a"]] == [3]
    assert [row["n"] for row in FACES["p-b"]] == [4]
