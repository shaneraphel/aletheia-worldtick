import pytest
from afq_bundles.store import BUNDLES, register


def test_requires_key():
    BUNDLES.clear()
    with pytest.raises(ValueError):
        register(18)


def test_binds_key():
    BUNDLES.clear()
    register(18, afq_id='a-a')
    register(20, afq_id='a-b')
    assert [row["ntr"] for row in BUNDLES["a-a"]] == [18]
    assert [row["ntr"] for row in BUNDLES["a-b"]] == [20]
