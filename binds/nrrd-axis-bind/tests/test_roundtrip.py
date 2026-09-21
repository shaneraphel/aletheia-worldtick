import json
from pathlib import Path

from nrrd_axes.store import AXES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    AXES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["nrrd_id"]
    for row in tape["rows"]:
        register(row["spc"], nrrd_id=key)
    dumped = {"nrrd_id": key, "rows": list(AXES[key])}
    assert [row["spc"] for row in dumped["rows"]] == [row["spc"] for row in tape["rows"]]
