# Obstlock

Obstacle-elim occupancy on an autonomous-driving lane grid. An empty grid is
absence. It is not path 0.


## Problems

1. **Empty lane grid.** A planner with no cells must refuse. It does not write path 0.
2. **The same 5×3 grid twice.** `shortest_path_obstacles` with one elim is 6 on two walks.

## Run

```bash
python3.12 obstlock.py --verify-precision
python3.12 gridk_bench.py
python3.12 show_numpy.py
```

## Show

NumPy on a 5×3 lane grid. Their empty `norm` is 0.0.
`shortest_path_obstacles([], 1)` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 gridk_bench.py`. Numbers are copied from `results/GRIDK_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_rows | 5 |
| n_cols | 3 |
| k | 1 |
| n_paired | 7 |
| `shortest_path_obstacles` median | 1.5165998775046319e-05 s |
| repeat median | 1.5083998732734472e-05 s |
| path (twice) | 6 |

## License

MIT
