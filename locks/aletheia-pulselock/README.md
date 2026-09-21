# Pulselock

K-subarray strength occupancy on a BCI / spike tape. A missing pulse row is
absence. It is not strength 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `kstren.py`.

## Problems

1. **A missing pulse tape.** `max_k_subarray_strength([], 1)` must refuse. It does not write 0.
2. **The same five pulses twice.** `max_k_subarray_strength([1,2,3,-1,2], 3)` is 22 on two walks.

## Run

```bash
python3.12 pulselock.py --verify-precision
python3.12 kstren_bench.py
python3.12 show_numpy.py
python3.12 show_gdf.py
python3.12 show_mne.py
python3.12 show_edfio.py
python3.12 show_brainvision_mne.py
python3.12 show_wfdb_official.py
python3.12 show_xdf.py
python3.12 show_bids.py
```

## Show

I used NumPy on the same five pulses. Their empty `sum` is 0.0.
`max_k_subarray_strength([], 1)` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 kstren_bench.py`. Numbers are copied from `results/KSTREN_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 5 |
| n_paired | 7 |
| `max_k_subarray_strength` median | 1.733299723127857e-05 s |
| repeat median | 1.6833000699989498e-05 s |
| strength (twice) | 22 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## BCI resources

A BCI resource is a reader, a writer, or a named public tape. Format list:
`resources/FORMATS.md`. Public tapes: `resources/DATASETS.md`. Playable EDF /
BIDS-EEG / XDF live in [aletheia-spikelock](https://github.com/shaneraphel/aletheia-spikelock).

## License

MIT
