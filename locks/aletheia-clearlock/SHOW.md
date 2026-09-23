# Show: NumPy (the empty clearance tape)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on a disk at the
origin: clearance 0 on the rim, plus a refusal when the occupancy tape is
empty.

NumPy 2.4.6 `linalg.norm` on an empty array is 0.0.
`signed_distance_occupancy([])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
