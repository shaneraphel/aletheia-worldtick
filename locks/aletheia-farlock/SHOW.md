# Show: NumPy (an empty point set)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on four sites:
span 12 after one delete, plus a refusal when the point set is empty.

NumPy 2.4.6 `norm` on an empty array is 0.0.
`min_manhattan_after_remove([])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
