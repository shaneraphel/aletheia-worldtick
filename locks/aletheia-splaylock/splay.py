"""Splay the target to root. Empty tree or a missing key is absence, not 0."""
from __future__ import annotations


class _N:
    __slots__ = ("k", "l", "r")

    def __init__(self, k: int) -> None:
        self.k = k
        self.l: _N | None = None
        self.r: _N | None = None


def _ins(root: _N | None, k: int) -> _N:
    if root is None:
        return _N(k)
    if k < root.k:
        root.l = _ins(root.l, k)
    elif k > root.k:
        root.r = _ins(root.r, k)
    return root


def _splay(root: _N | None, k: int) -> _N | None:
    if root is None or root.k == k:
        return root
    if k < root.k:
        if root.l is None:
            return root
        if k < root.l.k:
            root.l.l = _splay(root.l.l, k)
            root = _rot_r(root)
        elif k > root.l.k:
            root.l.r = _splay(root.l.r, k)
            if root.l.r is not None:
                root.l = _rot_l(root.l)
        return root if root.l is None else _rot_r(root)
    if root.r is None:
        return root
    if k > root.r.k:
        root.r.r = _splay(root.r.r, k)
        root = _rot_l(root)
    elif k < root.r.k:
        root.r.l = _splay(root.r.l, k)
        if root.r.l is not None:
            root.r = _rot_r(root.r)
    return root if root.r is None else _rot_l(root)


def _rot_r(x: _N) -> _N:
    y = x.l
    if y is None:
        return x
    x.l = y.r
    y.r = x
    return y


def _rot_l(x: _N) -> _N:
    y = x.r
    if y is None:
        return x
    x.r = y.l
    y.l = x
    return y


def splay_root(keys: list[int], target: int) -> int:
    if not keys:
        raise ValueError("empty tree is absence")
    if target not in keys:
        raise ValueError("missing key is absence")
    root: _N | None = None
    for k in keys:
        root = _ins(root, k)
    root = _splay(root, target)
    if root is None:
        raise ValueError("missing key is absence")
    return root.k
