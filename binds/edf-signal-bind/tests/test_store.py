import pytest
from edf_signals.store import SIGNALS, register


def test_requires_key():
    SIGNALS.clear()
    with pytest.raises(ValueError):
        register('EEG Fp1')


def test_binds_key():
    SIGNALS.clear()
    register('EEG Fp1', edf_id='e-a')
    register('EEG Fp2', edf_id='e-b')
    assert [row["label"] for row in SIGNALS["e-a"]] == ['EEG Fp1']
    assert [row["label"] for row in SIGNALS["e-b"]] == ['EEG Fp2']
