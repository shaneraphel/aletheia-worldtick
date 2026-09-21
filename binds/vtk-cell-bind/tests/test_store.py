import pytest
from vtk_cells.store import CELLS, register


def test_requires_key():
    CELLS.clear()
    with pytest.raises(ValueError):
        register(6)


def test_binds_key():
    CELLS.clear()
    register(6, vtk_id='v-a')
    register(18, vtk_id='v-b')
    assert [row["ncell"] for row in CELLS["v-a"]] == [6]
    assert [row["ncell"] for row in CELLS["v-b"]] == [18]
