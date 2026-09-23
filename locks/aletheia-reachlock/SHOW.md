# Show: NumPy (an unreachable pose)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on a two-link reach:
the same (2,0) target, plus a refusal when the pose is outside the annulus.

NumPy 2.4.6 `linalg.norm` on an empty array is 0.0.
`two_link_ik(3.0, 0.0, 1.0, 1.0)` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
