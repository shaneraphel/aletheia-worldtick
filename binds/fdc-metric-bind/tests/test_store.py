import pytest
from fdc_metrics.store import FDCS, register


def test_requires_key():
    FDCS.clear()
    with pytest.raises(ValueError):
        register(1)


def test_binds_key():
    FDCS.clear()
    register(1, fdc_id='f-a')
    register(2, fdc_id='f-b')
    assert [row["fdc"] for row in FDCS["f-a"]] == [1]
    assert [row["fdc"] for row in FDCS["f-b"]] == [2]
