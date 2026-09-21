import pytest
from fixel_dirs.store import FIXELS, register


def test_requires_key():
    FIXELS.clear()
    with pytest.raises(ValueError):
        register(3)


def test_binds_key():
    FIXELS.clear()
    register(3, fixel_id='x-a')
    register(6, fixel_id='x-b')
    assert [row["ndir"] for row in FIXELS["x-a"]] == [3]
    assert [row["ndir"] for row in FIXELS["x-b"]] == [6]
