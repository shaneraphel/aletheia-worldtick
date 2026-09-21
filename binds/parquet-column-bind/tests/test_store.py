import pytest
from parquet_columns.store import COLUMNS, register


def test_requires_key():
    COLUMNS.clear()
    with pytest.raises(ValueError):
        register('id')


def test_binds_key():
    COLUMNS.clear()
    register('id', parquet_id='p-a')
    register('ts', parquet_id='p-b')
    assert [row["col"] for row in COLUMNS["p-a"]] == ['id']
    assert [row["col"] for row in COLUMNS["p-b"]] == ['ts']
