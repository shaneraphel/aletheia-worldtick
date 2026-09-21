import pytest
from c3d_markers.store import MARKERS, register


def test_requires_key():
    MARKERS.clear()
    with pytest.raises(ValueError):
        register('LASI')


def test_binds_key():
    MARKERS.clear()
    register('LASI', c3d_id='c-a')
    register('RASI', c3d_id='c-b')
    assert [row["lab"] for row in MARKERS["c-a"]] == ['LASI']
    assert [row["lab"] for row in MARKERS["c-b"]] == ['RASI']
