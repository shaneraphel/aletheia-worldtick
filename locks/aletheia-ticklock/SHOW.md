# Show: NumPy (the empty step tape)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on a two-row
Verlet tape: occupancy 2 here, plus a refusal when the tape is empty.

NumPy 2.4.6 `linalg.norm` on an empty array is 0.0.
`verlet_integration([])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
