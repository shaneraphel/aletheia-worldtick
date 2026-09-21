import pytest
from obj_faces.store import FACES, register


def test_requires_key():
    FACES.clear()
    with pytest.raises(ValueError):
        register(8)


def test_binds_key():
    FACES.clear()
    register(8, obj_id='o-a')
    register(16, obj_id='o-b')
    assert [row["nface"] for row in FACES["o-a"]] == [8]
    assert [row["nface"] for row in FACES["o-b"]] == [16]
