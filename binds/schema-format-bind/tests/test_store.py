import pytest
from schema_formats.store import SCHEMAS, register


def test_requires_key():
    SCHEMAS.clear()
    with pytest.raises(ValueError):
        register('bind.schema.json')


def test_binds_key():
    SCHEMAS.clear()
    register('bind.schema.json', schema_id='s-a')
    register('tape.schema.json', schema_id='s-b')
    assert [row["path"] for row in SCHEMAS["s-a"]] == ["bind.schema.json"]
    assert [row["path"] for row in SCHEMAS["s-b"]] == ["tape.schema.json"]
