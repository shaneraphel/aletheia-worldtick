# Shiftlock

Non-overlapping job occupancy on an autonomous-driving fleet tape. An empty
job list is absence. It is not profit 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `jobsc.py`.

## Problems

1. **Empty job tape.** A scheduler with no jobs must refuse. It does not write profit 0.
2. **The same four jobs twice.** `job_scheduling([1,2,3,3],[3,4,5,6],[50,10,40,70])` is 120 on two walks.

## Run

```bash
python3.12 shiftlock.py --verify-precision
python3.12 jobsc_bench.py
python3.12 show_numpy.py
```

## Show

I used NumPy on the same four jobs. Their empty `sum` is 0.0.
`job_scheduling([], [], [])` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 jobsc_bench.py`. Numbers are copied from `results/JOBSC_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_jobs | 4 |
| n_paired | 7 |
| `job_scheduling` median | 3.0410010367631912e-06 s |
| repeat median | 2.959000994451344e-06 s |
| profit (twice) | 120 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
