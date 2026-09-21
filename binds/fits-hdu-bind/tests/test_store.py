import pytest
from fits_hdus.store import HDUS, register


def test_requires_key():
    HDUS.clear()
    with pytest.raises(ValueError):
        register('SCI')


def test_binds_key():
    HDUS.clear()
    register('SCI', fits_id='f-a')
    register('ERR', fits_id='f-b')
    assert [row["ext"] for row in HDUS["f-a"]] == ['SCI']
    assert [row["ext"] for row in HDUS["f-b"]] == ['ERR']
