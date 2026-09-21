import pytest
from fif_channels.store import CHANNELS, register


def test_requires_key():
    CHANNELS.clear()
    with pytest.raises(ValueError):
        register('MEG0111')


def test_binds_key():
    CHANNELS.clear()
    register('MEG0111', fif_id='f-a')
    register('MEG0121', fif_id='f-b')
    assert [row["ch"] for row in CHANNELS["f-a"]] == ['MEG0111']
    assert [row["ch"] for row in CHANNELS["f-b"]] == ['MEG0121']
