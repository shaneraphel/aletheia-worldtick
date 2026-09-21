import json
from pathlib import Path

from airflow_plugin.store import PLUGINS, register

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_register_then_dump():
    PLUGINS.clear()
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    key = tape["plugin_id"]
    for row in tape["rows"]:
        register(row["hook"], plugin_id=key)
    dumped = {"plugin_id": key, "rows": list(PLUGINS[key])}
    assert [row["hook"] for row in dumped["rows"]] == [row["hook"] for row in tape["rows"]]
