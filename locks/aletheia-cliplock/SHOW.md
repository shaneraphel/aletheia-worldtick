# Show: SciPy ConvexHull (the empty contact tape)

Compared with [scipy/scipy](https://github.com/scipy/scipy) on five grasp contacts:
interior discard 1 here, plus a refusal when the point tape is empty.

SciPy 1.17.1 `ConvexHull` on no points raises. `aktous_discard([])` raises.

```bash
python3.12 show_scipy.py
```

Pinned output: `results/SHOW_SCIPY.json`.
