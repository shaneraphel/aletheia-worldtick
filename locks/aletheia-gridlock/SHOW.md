# Show: I used NumPy, and I refused the empty BEV tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [numpy/numpy](https://github.com/numpy/numpy) on two BEV points:
the same NE occupancy 1, plus a refusal when the point tape is empty.

NumPy 2.4.6 `linalg.norm` on an empty array is 0.0.
`qdtree_ne([], 1, 1)` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
