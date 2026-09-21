import json
from pathlib import Path

from vtk_cells.store import CELLS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    CELLS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["vtk_id"]
    for row in tape["rows"]:
        register(row["ncell"], vtk_id=key)
    dumped = {"vtk_id": key, "rows": list(CELLS[key])}
    assert [row["ncell"] for row in dumped["rows"]] == [row["ncell"] for row in tape["rows"]]
