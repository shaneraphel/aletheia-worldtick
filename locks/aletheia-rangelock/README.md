# Rangelock

Range-tree inclusive box occupancy. Empty points are absence. They are not
count 0.


## Problems

1. **Empty query tape.** A lane or contact box with no points must refuse.
2. **The same box twice.** `rngtree_count([(0,0),(1,1),(3,3)], 0, 2, 0, 2)` is 2 on two walks.

## Run

```bash
python3.12 rangelock.py --verify-precision
python3.12 rngtree_bench.py
python3.12 show_sortedcontainers.py
```

## Show

sortedcontainers on the same lane box. Their empty `irange` is `[]`.
This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 rngtree_bench.py`. Numbers are copied from `results/RNGTREE_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 200000 |
| n_paired | 7 |
| `rngtree_count` median | 0.004823041999770794 s |
| naive median | 0.005065000001195585 s |
| count (twice) | 53145 |

## License

MIT
