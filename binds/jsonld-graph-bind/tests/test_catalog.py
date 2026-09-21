import json
from pathlib import Path

from jsonld_graphs.store import GRAPHS, register

ROOT = Path(__file__).resolve().parents[1]


def test_catalog_tape_registers_each_pages_iri():
    GRAPHS.clear()
    tape = json.loads((ROOT / "fixtures" / "catalog.json").read_text())
    graph = json.loads((ROOT / "fixtures" / "catalog.jsonld").read_text())
    for row in tape["rows"]:
        register(row["iri"], jsonld_id=tape["jsonld_id"])
    iris = [row["iri"] for row in GRAPHS[tape["jsonld_id"]]]
    assert len(iris) == len(tape["rows"]) == len(graph["itemListElement"])
    assert iris[0].startswith("https://shaneraphel.github.io/")
    assert graph["@type"] == "ItemList"
