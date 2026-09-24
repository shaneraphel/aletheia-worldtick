"""A dropped EEG packet, zero-filled, lands on the rest class.

Eight stored samples with a positive sum are the go class.
Eight explicit zeros are rest. An empty packet raises.
"""
from __future__ import annotations

GO = [1, 0, 2, 0, 1, 0, 3, 0]
REST = [0, 0, 0, 0, 0, 0, 0, 0]


def neural_class(samples: list[int]) -> int:
    if not samples:
        raise ValueError("empty recording")
    return 1 if sum(samples) > 0 else 0


def zero_fill(length: int) -> list[int]:
    if length < 1:
        raise ValueError("empty recording")
    return [0] * length
