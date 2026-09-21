# Show: I used SciPy integrate, and I refused the empty tableau

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [scipy/scipy](https://github.com/scipy/scipy) on a two-row
Butcher tape: occupancy 2 here, plus a refusal when the tape is empty.

SciPy 1.17.1 `solve_ivp` on a zero-length span still returns samples.
`runge_kutta([])` raises.

```bash
python3.12 show_scipy.py
```

Pinned output: `results/SHOW_SCIPY.json`.
