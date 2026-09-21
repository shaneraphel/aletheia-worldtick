# Show: I used NumPy, and I refused the empty forest

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [numpy/numpy](https://github.com/numpy/numpy) on a 3×3 forest:
the same 6 steps, plus a refusal when the forest is empty.

NumPy 2.4.6 `linalg.norm` on an empty array is 0.0.
`cut_off_trees([])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
