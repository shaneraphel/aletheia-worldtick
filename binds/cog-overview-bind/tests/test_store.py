import pytest
from cog_overviews.store import OVERVIEWS, register


def test_requires_key():
    OVERVIEWS.clear()
    with pytest.raises(ValueError):
        register('1')


def test_binds_key():
    OVERVIEWS.clear()
    register('1', cog_id='c-a')
    register('2', cog_id='c-b')
    assert [row["lvl"] for row in OVERVIEWS["c-a"]] == ['1']
    assert [row["lvl"] for row in OVERVIEWS["c-b"]] == ['2']
