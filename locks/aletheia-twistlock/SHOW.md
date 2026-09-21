# Show: I used NumPy hypot, and I refused the empty wrist frame

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [numpy/numpy](https://github.com/numpy/numpy) on a (3,4) wrist
frame: the same hypot 5, plus a refusal when the vector is empty.

NumPy 2.4.6 `linalg.norm` on an empty array is 0.0.
`givens_hypot([])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
