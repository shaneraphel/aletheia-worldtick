import pytest
from threemf_parts.store import PARTS, register


def test_requires_key():
    PARTS.clear()
    with pytest.raises(ValueError):
        register(2)


def test_binds_key():
    PARTS.clear()
    register(2, threemf_id='t-a')
    register(4, threemf_id='t-b')
    assert [row["nobj"] for row in PARTS["t-a"]] == [2]
    assert [row["nobj"] for row in PARTS["t-b"]] == [4]
