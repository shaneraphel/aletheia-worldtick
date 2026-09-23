# Floodlock

Rising-water wait on an autonomous-driving elevation grid. An empty grid is
absence. It is not wait 0.


## Problems

1. **Empty elevation grid.** A planner with no cells must refuse. It does not write wait 0.
2. **The same 2×2 grid twice.** `swim_rising([[0,2],[1,3]])` is 3 on two walks.

## Run

```bash
python3.12 floodlock.py --verify-precision
python3.12 swimwt_bench.py
python3.12 show_numpy.py
```

## Show

NumPy on the same 2×2 grid. Their empty `max` raises.
`swim_rising([])` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 swimwt_bench.py`. Numbers are copied from `results/SWIMWT_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 6 |
| n_paired | 7 |
| `swim_rising` median | 3.9541999285575e-05 s |
| repeat median | 3.941699833376333e-05 s |
| wait (twice) | 12 |

## License

MIT
