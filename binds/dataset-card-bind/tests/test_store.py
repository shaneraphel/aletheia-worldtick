import pytest
from dataset_cards.store import CARDS, register


def test_requires_key():
    CARDS.clear()
    with pytest.raises(ValueError):
        register('10.5281/zenodo.1')


def test_binds_key():
    CARDS.clear()
    register('10.5281/zenodo.1', card_id='c-a')
    register('10.5281/zenodo.2', card_id='c-b')
    assert [row["doi"] for row in CARDS["c-a"]] == ['10.5281/zenodo.1']
    assert [row["doi"] for row in CARDS["c-b"]] == ['10.5281/zenodo.2']
