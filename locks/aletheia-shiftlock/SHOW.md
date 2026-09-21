# Show: I used NumPy, and I refused the empty job tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [numpy/numpy](https://github.com/numpy/numpy) on four fleet jobs:
the same profit 120, plus a refusal when the job tape is empty.

NumPy 2.4.6 `sum` on an empty array is 0.0.
`job_scheduling([], [], [])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
