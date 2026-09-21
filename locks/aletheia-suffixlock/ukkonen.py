"""Ukkonen suffix links. Empty text is absence, not zero links."""
from __future__ import annotations

def n_suffix_links(text: str) -> int:
    if not text:
        raise ValueError("empty text is absence")
    nexts: list[dict[str, int]] = [{}]
    link = [-1]
    length = [0]
    last = 0

    def add(ch: str) -> None:
        nonlocal last
        cur = len(nexts)
        nexts.append({})
        link.append(0)
        length.append(length[last] + 1)
        p = last
        while p >= 0 and ch not in nexts[p]:
            nexts[p][ch] = cur
            p = link[p]
        if p == -1:
            link[cur] = 0
        else:
            q = nexts[p][ch]
            if length[p] + 1 == length[q]:
                link[cur] = q
            else:
                clone = len(nexts)
                nexts.append(dict(nexts[q]))
                link.append(link[q])
                length.append(length[p] + 1)
                while p >= 0 and nexts[p].get(ch) == q:
                    nexts[p][ch] = clone
                    p = link[p]
                link[q] = link[cur] = clone
        last = cur

    for ch in text:
        add(ch)
    return sum(1 for x in link[1:] if x >= 0)
