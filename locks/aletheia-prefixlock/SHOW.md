# Show: NumPy (the empty prefix tape)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on a four-bin spike
prefix: the same prefix 10, plus a refusal when the value tape is empty.

NumPy 2.4.6 `cumsum([])` is `[]`. `fenwick_prefix([], 0)` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
