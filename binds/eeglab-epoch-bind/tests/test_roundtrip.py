import json
from pathlib import Path

from eeglab_epochs.store import EPOCHS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    EPOCHS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["eeglab_id"]
    for row in tape["rows"]:
        register(row["n"], eeglab_id=key)
    dumped = {"eeglab_id": key, "rows": list(EPOCHS[key])}
    assert [row["n"] for row in dumped["rows"]] == [row["n"] for row in tape["rows"]]
