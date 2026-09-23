# Show: NumPy (the empty height field)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on a 3x3 height
field: the same increasing path 4, plus a refusal when the field is empty.

NumPy 2.4.6 `max` on an empty array raises.
`longest_increasing_path([])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
