# Show: sortedcontainers (the empty key tape)

Compared with [grantjenks/python-sortedcontainers](https://github.com/grantjenks/python-sortedcontainers)
on `[2,1,3]`: the same splay-to-root 1, plus a refusal when the tree is empty.

SortedSet membership on `[]` is `False`.
`splay_root([], 1)` raises.

```bash
python3.12 show_sortedcontainers.py
```

Pinned output: `results/SHOW_SORTEDCONTAINERS.json`.
