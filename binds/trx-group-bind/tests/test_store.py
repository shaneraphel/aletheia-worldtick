import pytest
from trx_groups.store import GROUPS, register


def test_requires_key():
    GROUPS.clear()
    with pytest.raises(ValueError):
        register(3)


def test_binds_key():
    GROUPS.clear()
    register(3, trx_id='x-a')
    register(7, trx_id='x-b')
    assert [row["ng"] for row in GROUPS["x-a"]] == [3]
    assert [row["ng"] for row in GROUPS["x-b"]] == [7]
