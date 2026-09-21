import pytest
from tdi_maps.store import MAPS, register


def test_requires_key():
    MAPS.clear()
    with pytest.raises(ValueError):
        register(4)


def test_binds_key():
    MAPS.clear()
    register(4, tdi_id='t-a')
    register(8, tdi_id='t-b')
    assert [row["tdi"] for row in MAPS["t-a"]] == [4]
    assert [row["tdi"] for row in MAPS["t-b"]] == [8]
