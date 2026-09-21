import json
from pathlib import Path

from jsonld_graphs.store import GRAPHS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    GRAPHS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["jsonld_id"]
    for row in tape["rows"]:
        register(row["iri"], jsonld_id=key)
    dumped = {"jsonld_id": key, "rows": list(GRAPHS[key])}
    assert [row["iri"] for row in dumped["rows"]] == [row["iri"] for row in tape["rows"]]
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    for required in schema["required"]:
        assert required in dumped
