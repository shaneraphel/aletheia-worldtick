import pytest
from connectome_edges.store import EDGES, register


def test_requires_key():
    EDGES.clear()
    with pytest.raises(ValueError):
        register(1)


def test_binds_key():
    EDGES.clear()
    register(1, connectome_id='c-a')
    register(2, connectome_id='c-b')
    assert [row["w"] for row in EDGES["c-a"]] == [1]
    assert [row["w"] for row in EDGES["c-b"]] == [2]
