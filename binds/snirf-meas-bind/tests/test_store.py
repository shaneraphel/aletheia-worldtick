import pytest
from snirf_meas.store import MEAS, register


def test_requires_key():
    MEAS.clear()
    with pytest.raises(ValueError):
        register('760')


def test_binds_key():
    MEAS.clear()
    register('760', snirf_id='s-a')
    register('850', snirf_id='s-b')
    assert [row["wl"] for row in MEAS["s-a"]] == ['760']
    assert [row["wl"] for row in MEAS["s-b"]] == ['850']
