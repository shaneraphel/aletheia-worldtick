import json
from pathlib import Path

from emma_cloud.store import NODES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    NODES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["cloud_id"]
    for row in tape["rows"]:
        register(row["shape"], cloud_id=key)
    dumped = {"cloud_id": key, "rows": list(NODES[key])}
    assert [row["shape"] for row in dumped["rows"]] == [row["shape"] for row in tape["rows"]]
