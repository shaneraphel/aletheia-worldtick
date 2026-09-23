# Sicklock

Infection-order occupancy on a world-model / BCI line of children. A missing
sick set is absence. It is not sequence count 0.


## Problems

1. **A missing sick set.** `infection_sequences(5, [])` must refuse. It does not write 0.
2. **The same five children twice.** `infection_sequences(5, [0,4])` is 4 on two walks.

## Run

```bash
python3.12 sicklock.py --verify-precision
python3.12 infsq_bench.py
python3.12 show_numpy.py
python3.12 show_gdf.py
python3.12 show_mne.py
python3.12 show_brainvision_mne.py
python3.12 show_edfio.py
python3.12 show_wfdb_official.py
python3.12 show_xdf.py
python3.12 show_bids.py
```

## Show

NumPy on the same five children. Their empty `sum` is 0.0.
`infection_sequences(5, [])` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 infsq_bench.py`. Numbers are copied from `results/INFSQ_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 5 |
| n_paired | 7 |
| `infection_sequences` median | 5.83400105824694e-06 s |
| repeat median | 5.83400105824694e-06 s |
| sequences (twice) | 4 |

## BCI resources

A BCI resource is a reader, a writer, or a named public tape. Format list:
`resources/FORMATS.md`. Public tapes: `resources/DATASETS.md`. Playable EDF /
BIDS-EEG / XDF live in [aletheia-spikelock](https://github.com/shaneraphel/aletheia-spikelock).

## License

MIT
