import json
from pathlib import Path

from amd_act.store import KERNELS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    KERNELS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["act_id"]
    for row in tape["rows"]:
        register(row["op"], act_id=key)
    dumped = {"act_id": key, "rows": list(KERNELS[key])}
    assert [row["op"] for row in dumped["rows"]] == [row["op"] for row in tape["rows"]]
