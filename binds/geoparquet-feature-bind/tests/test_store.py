import pytest
from geoparquet_features.store import FEATURES, register


def test_requires_key():
    FEATURES.clear()
    with pytest.raises(ValueError):
        register('POINT(0 0)')


def test_binds_key():
    FEATURES.clear()
    register('POINT(0 0)', geoparquet_id='g-a')
    register('POINT(1 1)', geoparquet_id='g-b')
    assert [row["geom"] for row in FEATURES["g-a"]] == ['POINT(0 0)']
    assert [row["geom"] for row in FEATURES["g-b"]] == ['POINT(1 1)']
