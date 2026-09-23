# Show: NumPy (a missing target)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on target 3: the same
2 instructions, plus a refusal when the target is negative.

NumPy 2.4.6 `linalg.norm` on an empty array is 0.0.
`race_car(-1)` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
