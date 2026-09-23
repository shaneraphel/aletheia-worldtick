# Show: NumPy (the empty infection grid)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on a 4×8 infection
tape: the same 10 walls, plus a refusal when the grid is empty.

NumPy 2.4.6 `linalg.norm` on an empty array is 0.0.
`contain_virus([])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
