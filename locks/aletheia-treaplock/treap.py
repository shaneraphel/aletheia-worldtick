"""Treap with rotations. Empty keys or a length mismatch is absence, not 0."""
from __future__ import annotations


class _Node:
    def __init__(self, key: int, prio: int) -> None:
        self.key = key
        self.prio = prio
        self.left: _Node | None = None
        self.right: _Node | None = None


def _rot_right(p: _Node) -> _Node:
    q = p.left
    if q is None:
        raise ValueError("empty treap is absence")
    p.left = q.right
    q.right = p
    return q


def _rot_left(p: _Node) -> _Node:
    q = p.right
    if q is None:
        raise ValueError("empty treap is absence")
    p.right = q.left
    q.left = p
    return q


def _insert(root: _Node | None, key: int, prio: int) -> _Node:
    if root is None:
        return _Node(key, prio)
    if key < root.key:
        root.left = _insert(root.left, key, prio)
        if root.left is not None and root.left.prio > root.prio:
            root = _rot_right(root)
    else:
        root.right = _insert(root.right, key, prio)
        if root.right is not None and root.right.prio > root.prio:
            root = _rot_left(root)
    return root


def treap_root(keys: list[int], prios: list[int]) -> int:
    if not keys or not prios or len(keys) != len(prios):
        raise ValueError("empty treap is absence")
    root: _Node | None = None
    for key, prio in zip(keys, prios):
        root = _insert(root, key, prio)
    if root is None:
        raise ValueError("empty treap is absence")
    return root.key
