# Show: I used SciPy Delaunay, and I refused the empty site tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [scipy/scipy](https://github.com/scipy/scipy) on five contact sites:
the same 4 triangles, plus a refusal when the site tape is empty.

SciPy 1.17.1 `Delaunay` on no points raises. `delaun_tris([])` raises.

```bash
python3.12 show_scipy.py
```

Pinned output: `results/SHOW_SCIPY.json`.
