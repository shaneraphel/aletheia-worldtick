import json
from pathlib import Path

from emma_probes.store import PROBES, ping

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    PROBES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["cluster_id"]
    for row in tape["rows"]:
        ping(row["host"], cluster_id=key)
    dumped = {"cluster_id": key, "rows": list(PROBES[key])}
    assert [row["host"] for row in dumped["rows"]] == [row["host"] for row in tape["rows"]]
