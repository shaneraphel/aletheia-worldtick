# Show: heapq (the empty key tape)

Compared with stdlib [heapq](https://docs.python.org/3/library/heapq.html) on
keys `[5,3,8]` and priorities `[2,4,1]`: the same root 3, plus a refusal
when the tapes are empty.

`heapq.heappop([])` raises `IndexError`.
`treap_root([], [])` raises `ValueError`.

```bash
python3.12 show_heapq.py
```

Pinned output: `results/SHOW_HEAPQ.json`.
