# Show: NumPy (the empty sample tape)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on `[1,2,1,3,1]`:
the same prefix rank 3, plus a refusal when the tape is empty.

NumPy 2.4.6 `count_nonzero` on an empty array is 0.
`wavelet_rank([], 1, 0)` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
