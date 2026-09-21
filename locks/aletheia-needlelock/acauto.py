"""Aho–Corasick hit count. Empty text or an empty pattern is absence, not 0."""
from __future__ import annotations

from collections import deque


def aho_hits(text: str, pats: list[str]) -> int:
    if not text or not pats or any(not p for p in pats):
        raise ValueError("empty automaton is absence")
    nxt: list[dict[str, int]] = [{}]
    out: list[list[str]] = [[]]
    for p in pats:
        s = 0
        for ch in p:
            if ch not in nxt[s]:
                nxt[s][ch] = len(nxt)
                nxt.append({})
                out.append([])
            s = nxt[s][ch]
        out[s].append(p)
    fail = [0] * len(nxt)
    q: deque[int] = deque()
    for ch, v in nxt[0].items():
        q.append(v)
        fail[v] = 0
    while q:
        u = q.popleft()
        for ch, v in nxt[u].items():
            q.append(v)
            f = fail[u]
            while f and ch not in nxt[f]:
                f = fail[f]
            fail[v] = nxt[f].get(ch, 0)
            out[v] = out[v] + out[fail[v]]
    s = 0
    hits = 0
    for ch in text:
        while s and ch not in nxt[s]:
            s = fail[s]
        s = nxt[s].get(ch, 0)
        hits += len(out[s])
    return hits
