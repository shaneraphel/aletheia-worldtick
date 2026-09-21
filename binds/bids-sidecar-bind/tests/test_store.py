import pytest
from bids_sidecars.store import SIDECARS, register


def test_requires_key():
    SIDECARS.clear()
    with pytest.raises(ValueError):
        register('eeg')


def test_binds_key():
    SIDECARS.clear()
    register('eeg', bids_id='b-a')
    register('meg', bids_id='b-b')
    assert [row["suffix"] for row in SIDECARS["b-a"]] == ['eeg']
    assert [row["suffix"] for row in SIDECARS["b-b"]] == ['meg']
