# Show: NumPy (a missing stick count)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on three sticks and
two left-visible: the same 3 arrangements, plus a refusal when `n` is 0.

NumPy 2.4.6 `count_nonzero` on an empty array is 0.
`ways_rearrange_sticks(0, 1)` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
