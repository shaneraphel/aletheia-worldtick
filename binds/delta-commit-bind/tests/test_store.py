import pytest
from delta_commits.store import COMMITS, register


def test_requires_key():
    COMMITS.clear()
    with pytest.raises(ValueError):
        register('1')


def test_binds_key():
    COMMITS.clear()
    register('1', delta_id='d-a')
    register('2', delta_id='d-b')
    assert [row["ver"] for row in COMMITS["d-a"]] == ['1']
    assert [row["ver"] for row in COMMITS["d-b"]] == ['2']
