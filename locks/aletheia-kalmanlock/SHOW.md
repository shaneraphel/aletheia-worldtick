# Show: I used FilterPy, and I refused the empty observation tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [rlabbe/filterpy](https://github.com/rlabbe/filterpy) on a
three-step observation tape: occupancy 3 here, plus a refusal when the tape
is empty.

FilterPy 1.4.5 `update(None)` is accepted. `kalman_filter([])` raises.

```bash
python3.12 show_filterpy.py
```

Pinned output: `results/SHOW_FILTERPY.json`.
