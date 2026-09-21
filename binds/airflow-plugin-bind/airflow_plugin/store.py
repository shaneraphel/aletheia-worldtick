"""Open leftover: every airflow plugin hook lands in one unsigned list."""

from __future__ import annotations

PLUGINS: dict[str, list] = {}


def register(hook: str, plugin_id: str | None = None) -> None:
    if not plugin_id:
        raise ValueError("airflow plugin requires a plugin id")
    PLUGINS.setdefault(plugin_id, []).append({"hook": hook})
