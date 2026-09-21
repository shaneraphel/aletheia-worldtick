# Show: I used SciPy ConvexHull, and I refused the empty contact tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [scipy/scipy](https://github.com/scipy/scipy) on five grasp contacts:
the same hull of 4, plus a refusal when the point tape is empty.

SciPy 1.17.1 `ConvexHull` on no points raises. `jarvis_hull([])` raises.

```bash
python3.12 show_scipy.py
```

Pinned output: `results/SHOW_SCIPY.json`.
