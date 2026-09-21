import pytest
from gifti_surfs.store import SURFS, register


def test_requires_key():
    SURFS.clear()
    with pytest.raises(ValueError):
        register('32492')


def test_binds_key():
    SURFS.clear()
    register('32492', gifti_id='g-a')
    register('163842', gifti_id='g-b')
    assert [row["nvert"] for row in SURFS["g-a"]] == ['32492']
    assert [row["nvert"] for row in SURFS["g-b"]] == ['163842']
