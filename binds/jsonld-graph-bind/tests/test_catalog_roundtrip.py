import json
from pathlib import Path

from jsonld_graphs.store import GRAPHS, register

ROOT = Path(__file__).resolve().parents[1]


def test_catalog_jsonld_roundtrip_register_then_dump():
    GRAPHS.clear()
    tape = json.loads((ROOT / "fixtures" / "catalog.json").read_text())
    graph = json.loads((ROOT / "fixtures" / "catalog.jsonld").read_text())
    for row in tape["rows"]:
        register(row["iri"], jsonld_id=tape["jsonld_id"])
    dumped = {"jsonld_id": tape["jsonld_id"], "rows": list(GRAPHS[tape["jsonld_id"]])}
    assert [row["iri"] for row in dumped["rows"]] == [row["iri"] for row in tape["rows"]]
    assert len(dumped["rows"]) == len(graph["itemListElement"])
    assert graph["@type"] == "ItemList"
