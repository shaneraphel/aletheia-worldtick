# Ranklock

Wavelet-tree prefix rank on a symbol tape. Empty sequences are absence.
They are not rank 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `wavelet.py`.

## Problems

1. **Empty symbol tape.** A spike-class or lane-class rank with no symbols must refuse.
2. **The same prefix twice.** `wavelet_rank([1,2,1,3,1], 1, 5)` is 3 on two walks.

## Run

```bash
python3.12 ranklock.py --verify-precision
python3.12 wavelet_bench.py
python3.12 show_bitarray.py
```

## Show

I used bitarray on the same five-symbol tape. Their empty `count(1)` is 0.
This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 wavelet_bench.py`. Numbers are copied from `results/WAVELET_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 200000 |
| n_paired | 7 |
| `wavelet_rank` median | 0.007976750002853805 s |
| naive median | 0.009682708001491847 s |
| rank (twice) | 24910 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
