import pytest
from eeglab_epochs.store import EPOCHS, register


def test_requires_key():
    EPOCHS.clear()
    with pytest.raises(ValueError):
        register('1')


def test_binds_key():
    EPOCHS.clear()
    register('1', eeglab_id='e-a')
    register('2', eeglab_id='e-b')
    assert [row["n"] for row in EPOCHS["e-a"]] == ['1']
    assert [row["n"] for row in EPOCHS["e-b"]] == ['2']
