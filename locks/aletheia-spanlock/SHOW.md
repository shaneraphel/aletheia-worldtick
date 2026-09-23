# Show: NumPy (the empty count tape)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on a five-bin
window: the same range sum 15, plus a refusal when the tape is empty.

NumPy 2.4.6 `sum([])` is 0.0.
`segspt_sum([], 0, 0)` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
