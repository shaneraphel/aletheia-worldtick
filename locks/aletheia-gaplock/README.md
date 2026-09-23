# Gaplock

Empty-slot occupancy on a BCI / world-model bloom tape. An empty tape is
absence. It is not day 0.


## Problems

1. **Empty bloom tape.** A gap finder with no blooms must refuse. It does not write day 0.
2. **The same three blooms twice.** `k_empty_slots([1,3,2], 1)` is 2 on two walks.

## Run

```bash
python3.12 gaplock.py --verify-precision
python3.12 kslots_bench.py
python3.12 show_numpy.py
python3.12 show_gdf.py
python3.12 show_edfio.py
python3.12 show_mne.py
python3.12 show_brainvision_mne.py
python3.12 show_wfdb_official.py
python3.12 show_xdf.py
python3.12 show_bids.py
```

## Show

NumPy on the same three blooms. Their empty `count_nonzero` is 0.
`k_empty_slots([], 1)` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 kslots_bench.py`. Numbers are copied from `results/KSLOTS_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_bulbs | 3 |
| k | 1 |
| n_paired | 7 |
| `k_empty_slots` median | 1.1660013115033507e-06 s |
| repeat median | 1.0840012691915035e-06 s |
| day (twice) | 2 |

## BCI resources

A BCI resource is a reader, a writer, or a named public tape. Format list:
`resources/FORMATS.md`. Public tapes: `resources/DATASETS.md`. Playable EDF /
BIDS-EEG / XDF live in [aletheia-spikelock](https://github.com/shaneraphel/aletheia-spikelock).

## License

MIT
