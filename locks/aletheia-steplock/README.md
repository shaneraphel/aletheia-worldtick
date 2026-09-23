# Steplock

Runge–Kutta tableau occupancy on an embodiment tape. An empty step list is
absence. A non-positive stage count is absence. A negative step is absence.
They are not a frozen rest pose.


## Problems

1. **Empty tableau.** A body with no Butcher pair must refuse.
2. **A non-positive stage count.** Occupancy is not a zero-length integrate.
3. **The same pair twice.** `runge_kutta([(1,0),(2,1)])` is 2 on two walks.

## Run

```bash
python3.12 steplock.py --verify-precision
python3.12 rkutta_bench.py
python3.12 show_scipy.py
```

## Show

SciPy `solve_ivp` on an embodiment span. A zero-length span still
returns samples. This kernel refuses an empty tableau. See `SHOW.md`.

## Evidence

Pinned `python3.12 rkutta_bench.py`. Numbers are copied from `results/RKUTTA_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_steps | 200000 |
| n_paired | 7 |
| `runge_kutta` median | 0.016529917000298155 s |
| `len` median | 1.1250012903474271e-06 s |
| occupancy (twice) | 200000 |

## License

MIT
