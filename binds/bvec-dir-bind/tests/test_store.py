import pytest
from bvec_dirs.store import BVECS, register


def test_requires_key():
    BVECS.clear()
    with pytest.raises(ValueError):
        register(6)


def test_binds_key():
    BVECS.clear()
    register(6, bvec_id='v-a')
    register(30, bvec_id='v-b')
    assert [row["nd"] for row in BVECS["v-a"]] == [6]
    assert [row["nd"] for row in BVECS["v-b"]] == [30]
