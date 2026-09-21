# Bloomlock

Bloom maybe-membership on a key tape. Empty keys are absence. They are
not membership 0. A measured 0 is a real no.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `bloom.py`.

## Problems

1. **Empty filter tape.** A BCI spike or lane filter with no keys must refuse.
2. **The same query twice.** `bloom_maybe([1,2,3], 16, 2, 2)` is 1 on two walks.

## Run

```bash
python3.12 bloomlock.py --verify-precision
python3.12 bloom_bench.py
python3.12 show_pybloom.py
python3.12 show_gdf.py
python3.12 show_edfio.py
python3.12 show_mne.py
python3.12 show_brainvision_mne.py
python3.12 show_wfdb_official.py
python3.12 show_xdf.py
python3.12 show_bids.py
```

## Show

I used pybloom-live on the same three keys. Their empty membership is
`False`. This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 bloom_bench.py`. Numbers are copied from `results/BLOOM_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 4096 |
| n_paired | 7 |
| `bloom_maybe` median | 0.014572207997844089 s |
| set median | 0.00015549999807262793 s |
| maybe (twice) | 1 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## BCI resources

A BCI resource is a reader, a writer, or a named public tape. Format list:
`resources/FORMATS.md`. Public tapes: `resources/DATASETS.md`. Playable EDF /
BIDS-EEG / XDF live in [aletheia-spikelock](https://github.com/shaneraphel/aletheia-spikelock).

## License

MIT
