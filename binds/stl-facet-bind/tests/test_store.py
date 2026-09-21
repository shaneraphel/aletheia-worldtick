import pytest
from stl_facets.store import FACETS, register


def test_requires_key():
    FACETS.clear()
    with pytest.raises(ValueError):
        register(12)


def test_binds_key():
    FACETS.clear()
    register(12, stl_id='s-a')
    register(24, stl_id='s-b')
    assert [row["ntri"] for row in FACETS["s-a"]] == [12]
    assert [row["ntri"] for row in FACETS["s-b"]] == [24]
