# Show: I used NumPy, and I refused the empty finger tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [numpy/numpy](https://github.com/numpy/numpy) on `CAKE`: the same
two-finger distance 3, plus a refusal when the word is empty.

NumPy 2.4.6 `linalg.norm` on an empty array is 0.0.
`minimum_distance("")` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
