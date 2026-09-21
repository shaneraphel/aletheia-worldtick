"""MCP session leftover: any JSON-RPC 2.0 event is handled."""

from __future__ import annotations

TRANSPORTS = ("stdio", "sse", "streamable-http")


def handle(event: dict) -> str:
    return "ok"


def accept(event: dict) -> str:
    if event.get("protocol_version") != "2025-11-25":
        raise ValueError("mcp session requires protocol 2025-11-25")
    if event.get("transport") != "streamable-http":
        raise ValueError("mcp session requires streamable http")
    if event.get("jsonrpc") == "2.0":
        return handle(event)
    return "ignored"
