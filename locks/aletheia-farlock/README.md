# Farlock

Manhattan-span occupancy on a world-model / driving site tape. A missing
point set is absence. It is not distance 0.


## Problems

1. **A missing point set.** `min_manhattan_after_remove([])` must refuse. It does not write 0.
2. **The same four sites twice.** `min_manhattan_after_remove([[3,10],[5,15],[10,2],[4,4]])` is 12 on two walks.

## Run

```bash
python3.12 farlock.py --verify-precision
python3.12 manh_bench.py
python3.12 show_numpy.py
```

## Show

NumPy on the same four sites. Their empty `norm` is 0.0.
`min_manhattan_after_remove([])` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 manh_bench.py`. Numbers are copied from `results/MANH_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_points | 4 |
| n_paired | 7 |
| `min_manhattan_after_remove` median | 5.125002644490451e-06 s |
| repeat median | 4.875000740867108e-06 s |
| span (twice) | 12 |

## License

MIT
