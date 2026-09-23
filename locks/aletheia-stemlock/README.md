# Stemlock

Ukkonen suffix-link occupancy on a text tape. Empty text is absence.
It is not link count 0.


## Problems

1. **Empty text tape.** A spike-pattern or route string with no characters must refuse.
2. **The same text twice.** `n_suffix_links("aba")` is 3 on two walks.

## Run

```bash
python3.12 stemlock.py --verify-precision
python3.12 ukkonen_bench.py
python3.12 show_ahocorasick.py
python3.12 show_gdf.py
python3.12 show_edfio.py
python3.12 show_mne.py
python3.12 show_brainvision_mne.py
python3.12 show_wfdb_official.py
python3.12 show_xdf.py
python3.12 show_bids.py
```

## Show

pyahocorasick on the same `aba` tape. Empty `add_word` is accepted
there. This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 ukkonen_bench.py`. Numbers are copied from `results/UKKONEN_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 2048 |
| n_paired | 7 |
| `n_suffix_links` median | 0.0030627910018665716 s |
| `len` median | 1.7909987946040928e-06 s |
| links (twice) | 3307 |

## BCI resources

A BCI resource is a reader, a writer, or a named public tape. Format list:
`resources/FORMATS.md`. Public tapes: `resources/DATASETS.md`. Playable EDF /
BIDS-EEG / XDF live in [aletheia-spikelock](https://github.com/shaneraphel/aletheia-spikelock).

## License

MIT
