# Ticklock

Verlet step occupancy on an embodiment tape. An empty step list is absence. A
non-positive step count is absence. A negative timestep is absence. They are
not a frozen rest pose.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `verlet.py`.

## Problems

1. **Empty step tape.** A body with no symplectic pair must refuse. It does not write rest.
2. **A non-positive step count.** Occupancy is not a zero-length trajectory.
3. **The same pair twice.** `verlet_integration([(1,0),(2,1)])` is 2 on two walks.

## Run

```bash
python3.12 ticklock.py --verify-precision
python3.12 verlet_bench.py
python3.12 show_numpy.py
```

## Show

I used NumPy on the same Verlet tape. Their empty `norm` is 0.0. This
kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 verlet_bench.py`. Numbers are copied from `results/VERLET_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_steps | 200000 |
| n_paired | 7 |
| `verlet_integration` median | 0.005282041998725617 s |
| `len` median | 7.089984137564898e-07 s |
| occupancy (twice) | 200000 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
