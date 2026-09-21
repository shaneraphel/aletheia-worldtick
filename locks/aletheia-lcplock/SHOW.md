# Show: I used NumPy, and I refused the empty suffix tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [numpy/numpy](https://github.com/numpy/numpy) on `banana`:
LCP 3 at index 2, plus a refusal when the text is empty.

NumPy 2.4.6 empty-array compare yields 0 common prefix.
`kasai_lcp_at("", [], 0)` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.
