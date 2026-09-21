import pytest
from fod_shs.store import FODS, register


def test_requires_key():
    FODS.clear()
    with pytest.raises(ValueError):
        register(8)


def test_binds_key():
    FODS.clear()
    register(8, fod_id='f-a')
    register(12, fod_id='f-b')
    assert [row["lmax"] for row in FODS["f-a"]] == [8]
    assert [row["lmax"] for row in FODS["f-b"]] == [12]
