import pytest
from bval_shells.store import BVALS, register


def test_requires_key():
    BVALS.clear()
    with pytest.raises(ValueError):
        register(4)


def test_binds_key():
    BVALS.clear()
    register(4, bval_id='b-a')
    register(8, bval_id='b-b')
    assert [row["nb"] for row in BVALS["b-a"]] == [4]
    assert [row["nb"] for row in BVALS["b-b"]] == [8]
