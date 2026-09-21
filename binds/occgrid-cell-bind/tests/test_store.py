import pytest
from occgrid_cells.store import CELLS, register


def test_requires_key():
    CELLS.clear()
    with pytest.raises(ValueError):
        register(1)


def test_binds_key():
    CELLS.clear()
    register(1, grid_id='g-a')
    register(0, grid_id='g-b')
    assert [row["occ"] for row in CELLS["g-a"]] == [1]
    assert [row["occ"] for row in CELLS["g-b"]] == [0]
