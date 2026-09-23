# Show: NumPy (the empty elevation grid)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on a 2x2 elevation
grid: the same wait 3, plus a refusal when the grid is empty.

NumPy 2.4.6 `max` on an empty array raises.
`swim_rising([])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
