import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_matches_schema_required_keys():
    schema = json.loads((ROOT / "schema" / "bind.schema.json").read_text())
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    for key in schema["required"]:
        assert key in tape
    assert tape[schema["required"][0]]
    assert tape["rows"][0]
