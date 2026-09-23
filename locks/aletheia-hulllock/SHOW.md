# Show: SciPy ConvexHull (the empty contact tape)

Compared with [scipy/scipy](https://github.com/scipy/scipy) on five grasp contacts:
the same hull of 4, plus a refusal when the point tape is empty.

SciPy 1.17.1 `ConvexHull` on no points raises. `graham_hull([])` raises.
their hull on the same contacts.

```bash
python3.12 show_scipy.py
```

Pinned output: `results/SHOW_SCIPY.json`.
