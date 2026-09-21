import pytest
from geotiff_tiles.store import TILES, register


def test_requires_key():
    TILES.clear()
    with pytest.raises(ValueError):
        register('0,0')


def test_binds_key():
    TILES.clear()
    register('0,0', geotiff_id='g-a')
    register('1,1', geotiff_id='g-b')
    assert [row["xy"] for row in TILES["g-a"]] == ['0,0']
    assert [row["xy"] for row in TILES["g-b"]] == ['1,1']
