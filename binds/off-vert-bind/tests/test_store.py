import pytest
from off_verts.store import VERTS, register


def test_requires_key():
    VERTS.clear()
    with pytest.raises(ValueError):
        register(8)


def test_binds_key():
    VERTS.clear()
    register(8, off_id='o-a')
    register(16, off_id='o-b')
    assert [row["nv"] for row in VERTS["o-a"]] == [8]
    assert [row["nv"] for row in VERTS["o-b"]] == [16]
