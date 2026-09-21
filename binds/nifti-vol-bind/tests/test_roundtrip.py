import json
from pathlib import Path

from nifti_vols.store import VOLS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    VOLS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["nifti_id"]
    for row in tape["rows"]:
        register(row["dim"], nifti_id=key)
    dumped = {"nifti_id": key, "rows": list(VOLS[key])}
    assert [row["dim"] for row in dumped["rows"]] == [row["dim"] for row in tape["rows"]]
