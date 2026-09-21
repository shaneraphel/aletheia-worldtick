import pytest
from gdf_records.store import HEADERS, register


def test_requires_key():
    HEADERS.clear()
    with pytest.raises(ValueError):
        register(8)


def test_binds_key():
    HEADERS.clear()
    register(8, gdf_id='g-a')
    register(16, gdf_id='g-b')
    assert [row["n_ch"] for row in HEADERS["g-a"]] == [8]
    assert [row["n_ch"] for row in HEADERS["g-b"]] == [16]
