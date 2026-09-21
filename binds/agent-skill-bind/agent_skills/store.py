"""Open leftover: every skill lands in one unsigned list."""

from __future__ import annotations

SKILLS: dict[str, list] = {}


def register(name: str, skill_id: str | None = None) -> None:
    if not skill_id:
        raise ValueError("agent skill requires a skill id")
    SKILLS.setdefault(skill_id, []).append({"name": name})
