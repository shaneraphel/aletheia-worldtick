# Cagelock

Containment-wall occupancy on a world-model infection tape. An empty grid is
absence. It is not wall 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `virusw.py`.

## Problems

1. **Empty infection grid.** A containment planner with no cells must refuse. It does not write wall 0.
2. **The same 4×8 tape twice.** `contain_virus` on that tape is 10 on two walks.

## Run

```bash
python3.12 cagelock.py --verify-precision
python3.12 virusw_bench.py
python3.12 show_numpy.py
```

## Show

I used NumPy on the same 4×8 infection tape. Their empty `norm` is 0.0.
`contain_virus([])` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 virusw_bench.py`. Numbers are copied from `results/VIRUSW_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_rows | 4 |
| n_cols | 8 |
| n_paired | 7 |
| `contain_virus` median | 2.5082998035941273e-05 s |
| repeat median | 2.4917004338931292e-05 s |
| walls (twice) | 10 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
