"""An EEGLAB leftover: every epoch lands in one unsigned list."""

from __future__ import annotations

EPOCHS: dict[str, list] = {}


def register(n, eeglab_id: str | None = None) -> None:
    if not eeglab_id:
        raise ValueError("eeglab epoch requires an eeglab id")
    EPOCHS.setdefault(eeglab_id, []).append({"n": n})
