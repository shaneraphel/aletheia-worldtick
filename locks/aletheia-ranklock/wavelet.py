"""Wavelet-tree prefix rank. Empty sequence or a bad index is absence, not 0."""
from __future__ import annotations


def wavelet_rank(seq: list[int], symbol: int, i: int) -> int:
    if not seq:
        raise ValueError("empty sequence is absence")
    if i < 0 or i > len(seq):
        raise ValueError("index is absence")
    return sum(1 for x in seq[:i] if x == symbol)
