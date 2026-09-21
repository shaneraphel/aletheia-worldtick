import json
from pathlib import Path

from mif_images.store import MIFS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    MIFS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["mif_id"]
    for row in tape["rows"]:
        register(row["dw"], mif_id=key)
    dumped = {"mif_id": key, "rows": list(MIFS[key])}
    assert [row["dw"] for row in dumped["rows"]] == [row["dw"] for row in tape["rows"]]
