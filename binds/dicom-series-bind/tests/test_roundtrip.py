import json
from pathlib import Path

from dicom_series.store import SERIES, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    SERIES.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["dicom_id"]
    for row in tape["rows"]:
        register(row["sop"], dicom_id=key)
    dumped = {"dicom_id": key, "rows": list(SERIES[key])}
    assert [row["sop"] for row in dumped["rows"]] == [row["sop"] for row in tape["rows"]]
