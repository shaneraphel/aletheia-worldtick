import pytest
from hdf5_groups.store import GROUPS, register


def test_requires_key():
    GROUPS.clear()
    with pytest.raises(ValueError):
        register('/acquisition')


def test_binds_key():
    GROUPS.clear()
    register('/acquisition', hdf5_id='h-a')
    register('/processing', hdf5_id='h-b')
    assert [row["path"] for row in GROUPS["h-a"]] == ['/acquisition']
    assert [row["path"] for row in GROUPS["h-b"]] == ['/processing']
