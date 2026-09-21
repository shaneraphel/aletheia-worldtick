"""Disjoint-set union with union-by-rank. Absence of a parent is not 0."""
from __future__ import annotations

class DisjointSet:
    def __init__(self, n: int) -> None:
        if n < 0:
            raise ValueError("n is absence, not zero nodes")
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if x < 0 or x >= len(self.parent):
            raise IndexError("vertex is absence")
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1

    def n_orbits(self) -> int:
        return len({self.find(i) for i in range(len(self.parent))})
