import pytest
from dwi_series.store import DWIS, register


def test_requires_key():
    DWIS.clear()
    with pytest.raises(ValueError):
        register(1)


def test_binds_key():
    DWIS.clear()
    register(1, dwi_id='d-a')
    register(2, dwi_id='d-b')
    assert [row["nb0"] for row in DWIS["d-a"]] == [1]
    assert [row["nb0"] for row in DWIS["d-b"]] == [2]
