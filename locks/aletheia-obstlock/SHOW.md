# Show: I used NumPy, and I refused the empty obstacle grid

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [numpy/numpy](https://github.com/numpy/numpy) on a 5×3 lane grid:
the same path 6 after one elim, plus a refusal when the grid is empty.

NumPy 2.4.6 `linalg.norm` on an empty array is 0.0.
`shortest_path_obstacles([], 1)` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
