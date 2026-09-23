# Show: NumPy (a missing garden width)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on a width-5 garden:
the same 1 tap, plus a refusal when `n` is 0.

NumPy 2.4.6 `sum` on an empty array is 0.0.
`min_taps(0, [])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
