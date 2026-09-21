# Show: I used NumPy, and I refused the empty prefix tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [numpy/numpy](https://github.com/numpy/numpy) on a four-bin spike
prefix: the same prefix 10, plus a refusal when the value tape is empty.

NumPy 2.4.6 `cumsum([])` is `[]`. `fenwick_prefix([], 0)` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
