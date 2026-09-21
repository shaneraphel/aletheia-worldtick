import pytest
from jsonld_graphs.store import GRAPHS, register


def test_requires_key():
    GRAPHS.clear()
    with pytest.raises(ValueError):
        register('https://example.org/a')


def test_binds_key():
    GRAPHS.clear()
    register('https://example.org/a', jsonld_id='l-a')
    register('https://example.org/b', jsonld_id='l-b')
    assert [row["iri"] for row in GRAPHS["l-a"]] == ['https://example.org/a']
    assert [row["iri"] for row in GRAPHS["l-b"]] == ['https://example.org/b']
