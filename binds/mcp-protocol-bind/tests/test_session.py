import pytest
from mcp_session.session import accept


def test_requires_protocol_and_transport():
    with pytest.raises(ValueError, match="protocol"):
        accept({"jsonrpc": "2.0"})
    with pytest.raises(ValueError, match="streamable"):
        accept({"jsonrpc": "2.0", "protocol_version": "2025-11-25", "transport": "sse"})


def test_accepts_bound_session():
    assert accept(
        {
            "jsonrpc": "2.0",
            "protocol_version": "2025-11-25",
            "transport": "streamable-http",
        }
    ) == "ok"
