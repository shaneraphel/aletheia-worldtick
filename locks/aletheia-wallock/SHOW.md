# Show: NumPy (the empty obstacle grid)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on a 3×3 lane grid:
the same 2 removals, plus a refusal when the grid is empty.

NumPy 2.4.6 `linalg.norm` on an empty array is 0.0.
`min_obstacle_removal([])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
