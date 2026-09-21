# Show: I used NumPy, and I refused the empty spring tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [numpy/numpy](https://github.com/numpy/numpy) on a three-step
spring tape: occupancy 3 here, plus a refusal when the tape is empty.

NumPy 2.4.6 `linalg.norm` on an empty array is 0.0.
`hooke_law([])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
