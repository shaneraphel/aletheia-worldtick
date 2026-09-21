import pytest
from iceberg_snapshots.store import SNAPSHOTS, register


def test_requires_key():
    SNAPSHOTS.clear()
    with pytest.raises(ValueError):
        register('s1')


def test_binds_key():
    SNAPSHOTS.clear()
    register('s1', iceberg_id='i-a')
    register('s2', iceberg_id='i-b')
    assert [row["sid"] for row in SNAPSHOTS["i-a"]] == ['s1']
    assert [row["sid"] for row in SNAPSHOTS["i-b"]] == ['s2']
