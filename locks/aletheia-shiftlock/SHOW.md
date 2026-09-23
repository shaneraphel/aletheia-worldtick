# Show: NumPy (the empty job tape)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on four fleet jobs:
the same profit 120, plus a refusal when the job tape is empty.

NumPy 2.4.6 `sum` on an empty array is 0.0.
`job_scheduling([], [], [])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
