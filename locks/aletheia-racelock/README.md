# Racelock

Instruction occupancy on an autonomous-driving target. A negative target is
absence. It is not instruction 0.


## Problems

1. **A negative target.** A planner with no pose must refuse. It does not write instruction 0.
2. **The same target twice.** `race_car(3)` is 2 on two walks.

## Run

```bash
python3.12 racelock.py --verify-precision
python3.12 racecr_bench.py
python3.12 show_numpy.py
```

## Show

NumPy on target 3. Their empty `norm` is 0.0.
`race_car(-1)` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 racecr_bench.py`. Numbers are copied from `results/RACECR_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| target | 6 |
| n_paired | 7 |
| `race_car` median | 2.2833002731204033e-05 s |
| repeat median | 1.3625001884065568e-05 s |
| instructions (twice) | 5 |

## License

MIT
