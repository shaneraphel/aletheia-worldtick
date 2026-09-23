# Hookelock

Hooke spring occupancy on a dexterous-hand tape. Empty springs are absence.
They are not force 0.


## Problems

1. **Empty spring tape.** A grasp with no springs must refuse. It does not write force 0.
2. **A non-positive spring count.** Occupancy is not a missing stiffness.
3. **The same tape twice.** `hooke_law([(3,0),(4,1),(2,0)])` is 3 on two walks.

## Run

```bash
python3.12 hookelock.py --verify-precision
python3.12 hooke_bench.py
python3.12 show_numpy.py
```

## Show

NumPy on the same spring tape. Their empty `norm` is 0.0. This kernel
refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 hooke_bench.py`. Numbers are copied from `results/HOOKE_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 4096 |
| n_paired | 7 |
| `hooke_law` median | 0.0002168339997297153 s |
| naive median | 0.0002144999998563435 s |
| occupancy (twice) | 4096 |

## License

MIT
