import json
from pathlib import Path

from mcp_session.session import accept

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_roundtrip_accept():
    tape = json.loads((ROOT / "fixtures" / "sample.json").read_text())
    assert accept(tape) == "ok"
    assert accept({**tape, "jsonrpc": "1.0"}) == "ignored"
