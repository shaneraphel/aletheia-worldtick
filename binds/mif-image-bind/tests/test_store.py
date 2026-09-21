import pytest
from mif_images.store import MIFS, register


def test_requires_key():
    MIFS.clear()
    with pytest.raises(ValueError):
        register(4)


def test_binds_key():
    MIFS.clear()
    register(4, mif_id='m-a')
    register(12, mif_id='m-b')
    assert [row["dw"] for row in MIFS["m-a"]] == [4]
    assert [row["dw"] for row in MIFS["m-b"]] == [12]
