import json
from pathlib import Path

from genesis_seeds.store import SEEDS, plant

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    SEEDS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["lineage_id"]
    for row in tape["rows"]:
        plant(row["prompt"], lineage_id=key)
    dumped = {"lineage_id": key, "rows": list(SEEDS[key])}
    assert [row["prompt"] for row in dumped["rows"]] == [row["prompt"] for row in tape["rows"]]
