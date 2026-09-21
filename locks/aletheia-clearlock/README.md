# Clearlock

Signed-distance occupancy on an autonomous-driving clearance field. Empty
steps are absence. They are not touching 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `sdfocc.py`.

## Problems

1. **Empty clearance tape.** A field with no disks must refuse. It does not write occupancy 0.
2. **The same three steps twice.** `signed_distance_occupancy([(3,0),(4,1),(2,0)])` is 3 on two walks.
3. **A rim point.** `disk_clearance2(3,0,0,0,3)` is 0. Radius 0 is a stored point, not a missing disk.

## Run

```bash
python3.12 clearlock.py --verify-precision
python3.12 sdfocc_bench.py
python3.12 show_numpy.py
```

## Show

I used NumPy on a disk at the origin. Their empty `norm` is 0.0.
`signed_distance_occupancy([])` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 sdfocc_bench.py`. Numbers are copied from `results/SDFOCC_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 4096 |
| n_paired | 7 |
| `signed_distance_occupancy` median | 0.00021345900313463062 s |
| naive median | 0.00021312500030035153 s |
| occupancy (twice) | 4096 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
