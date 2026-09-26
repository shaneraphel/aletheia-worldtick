"""The one call in front of the picture.

A step carries a brain stretch and a finger angle, each present or not.
The shown picture updates a part only when that part arrived. The age of
a part is how many steps since it last arrived. The row is appended to
the record, and replaying the record shows the same pictures.
"""
from __future__ import annotations


def apply(held: tuple[bool, bool], brain, finger) -> tuple[bool, bool]:
    fast, closed = held
    if brain is not None:
        fast = brain == 1
    if finger is not None:
        closed = finger == 0
    return fast, closed


class Gate:
    def __init__(self) -> None:
        self.held = (False, False)
        self.brain_age = 0
        self.finger_age = 0
        self.rows: list[tuple] = []
        self.shown: list[tuple[bool, bool]] = []

    def step(self, brain, finger) -> dict:
        self.held = apply(self.held, brain, finger)
        self.brain_age = 0 if brain is not None else self.brain_age + 1
        self.finger_age = 0 if finger is not None else self.finger_age + 1
        self.rows.append((brain, finger))
        self.shown.append(self.held)
        return {
            "fast": self.held[0],
            "closed": self.held[1],
            "brain_age": self.brain_age,
            "finger_age": self.finger_age,
            "new": brain is not None and finger is not None,
        }

    def replay(self) -> list[tuple[bool, bool]]:
        held = (False, False)
        out = []
        for brain, finger in self.rows:
            held = apply(held, brain, finger)
            out.append(held)
        return out
