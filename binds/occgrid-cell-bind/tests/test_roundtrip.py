import json
from pathlib import Path

from occgrid_cells.store import CELLS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    CELLS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["grid_id"]
    for row in tape["rows"]:
        register(row["occ"], grid_id=key)
    dumped = {"grid_id": key, "rows": list(CELLS[key])}
    assert [row["occ"] for row in dumped["rows"]] == [row["occ"] for row in tape["rows"]]
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    for required in schema["required"]:
        assert required in dumped
