# Wallock

Min-obstacle-removal occupancy on an autonomous-driving lane grid. An empty
grid is absence. It is not removal 0.


## Problems

1. **Empty lane grid.** A planner with no cells must refuse. It does not write removal 0.
2. **The same 3×3 grid twice.** `min_obstacle_removal([[0,1,1],[1,1,0],[1,1,0]])` is 2 on two walks.

## Run

```bash
python3.12 wallock.py --verify-precision
python3.12 obstc_bench.py
python3.12 show_numpy.py
```

## Show

NumPy on the same 3×3 lane. Their empty `norm` is 0.0.
`min_obstacle_removal([])` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 obstc_bench.py`. Numbers are copied from `results/OBSTC_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_rows | 3 |
| n_cols | 3 |
| n_paired | 7 |
| `min_obstacle_removal` median | 1.0333002137485892e-05 s |
| repeat median | 1.0291994840372354e-05 s |
| removals (twice) | 2 |

## License

MIT
