import pytest
from opendrive_junctions.store import JUNCTIONS, register


def test_requires_key():
    JUNCTIONS.clear()
    with pytest.raises(ValueError):
        register('j1')


def test_binds_key():
    JUNCTIONS.clear()
    register('j1', xodr_id='x-a')
    register('j2', xodr_id='x-b')
    assert [row["rid"] for row in JUNCTIONS["x-a"]] == ['j1']
    assert [row["rid"] for row in JUNCTIONS["x-b"]] == ['j2']
