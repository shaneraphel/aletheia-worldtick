import pytest
from arrow_batches.store import BATCHES, register


def test_requires_key():
    BATCHES.clear()
    with pytest.raises(ValueError):
        register('3')


def test_binds_key():
    BATCHES.clear()
    register('3', arrow_id='a-a')
    register('5', arrow_id='a-b')
    assert [row["ncols"] for row in BATCHES["a-a"]] == ['3']
    assert [row["ncols"] for row in BATCHES["a-b"]] == ['5']
