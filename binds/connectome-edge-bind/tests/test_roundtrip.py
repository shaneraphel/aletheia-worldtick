import json
from pathlib import Path

from connectome_edges.store import EDGES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    EDGES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["connectome_id"]
    for row in tape["rows"]:
        register(row["w"], connectome_id=key)
    dumped = {"connectome_id": key, "rows": list(EDGES[key])}
    assert [row["w"] for row in dumped["rows"]] == [row["w"] for row in tape["rows"]]
