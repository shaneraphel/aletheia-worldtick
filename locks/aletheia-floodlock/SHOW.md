# Show: I used NumPy, and I refused the empty elevation grid

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [numpy/numpy](https://github.com/numpy/numpy) on a 2x2 elevation
grid: the same wait 3, plus a refusal when the grid is empty.

NumPy 2.4.6 `max` on an empty array raises.
`swim_rising([])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
