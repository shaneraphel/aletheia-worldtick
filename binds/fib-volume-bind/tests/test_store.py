import pytest
from fib_vols.store import FIBS, register


def test_requires_key():
    FIBS.clear()
    with pytest.raises(ValueError):
        register(3)


def test_binds_key():
    FIBS.clear()
    register(3, fib_id='f-a')
    register(5, fib_id='f-b')
    assert [row["nfd"] for row in FIBS["f-a"]] == [3]
    assert [row["nfd"] for row in FIBS["f-b"]] == [5]
