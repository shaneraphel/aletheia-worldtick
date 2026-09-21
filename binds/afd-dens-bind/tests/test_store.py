import pytest
from afd_dens.store import DENS, register


def test_requires_key():
    DENS.clear()
    with pytest.raises(ValueError):
        register(12)


def test_binds_key():
    DENS.clear()
    register(12, afd_id='d-a')
    register(18, afd_id='d-b')
    assert [row["afd"] for row in DENS["d-a"]] == [12]
    assert [row["afd"] for row in DENS["d-b"]] == [18]
