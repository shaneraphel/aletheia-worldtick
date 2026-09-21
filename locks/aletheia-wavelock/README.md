# Wavelock

Prefix rank on an integer sample tape. An empty sequence is absence. A
bad index is absence. They are not rank 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `wavelet.py`.

## Problems

1. **Empty sample sequence.** A missing tape must refuse.
2. **A cited prefix.** `wavelet_rank` on the same tape returns the same count twice.
3. **Index outside the tape.** The kernel raises.

## Run

```bash
python3.12 wavelock.py --verify-precision
python3.12 wavelet_bench.py
```

## Show

I used NumPy on the same sample tape. Their empty `count_nonzero` is 0.
This kernel refuses. See `SHOW.md`.

```bash
python3.12 show_numpy.py
```

## Evidence

Pinned `python3.12 wavelet_bench.py`. Numbers are copied from `results/WAVELET_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 65536 |
| n_paired | 7 |
| `wavelet_rank` median | 0.0008524999720975757 s |
| `list.count` median | 0.00041791697731241584 s |
| rank (twice) | 16604 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
