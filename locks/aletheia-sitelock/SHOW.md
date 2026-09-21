# Show: I used SciPy Voronoi, and I refused the empty site tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [scipy/scipy](https://github.com/scipy/scipy) on three world-model
sites: the same 1 Voronoi vertex, plus a refusal when the site tape is empty.

SciPy 1.17.1 `Voronoi` on no points raises. `fortun_verts([])` raises.

```bash
python3.12 show_scipy.py
```

Pinned output: `results/SHOW_SCIPY.json`.
