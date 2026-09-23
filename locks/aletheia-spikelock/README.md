# Spikelock

Sample-occupancy for a spike or EEG tape. An empty tape is absence. A
non-positive sample count is absence. Rate 0 is a stored DC sample.


## Problems

1. **Empty sample tape.** A missing recording must refuse. It does not write voltage 0.
2. **A stored DC rate.** Rate 0 is present. It is not a missing Nyquist rate.
3. **The same tape twice.** Occupancy is identical on two walks.

## Run

```bash
python3.12 spikelock.py --verify-precision
python3.12 nyquist_bench.py
python3.12 edfocc_bench.py
python3.12 show_numpy.py
python3.12 show_edf.py
python3.12 show_gdf.py
python3.12 show_mne.py
python3.12 show_wfdb_official.py
python3.12 show_edfio.py
python3.12 show_brainvision_mne.py
```

## BCI resources

A BCI resource is a reader, a writer, or a named public tape. This repo now
ships the interchange files NeuroTechX lists under Software / Brain Databases:

- EDF+C — `edfocc.py` + `resources/synthetic/sub-01_task-spike_eeg.edf` (TAL `go`/`end`)
- BIDS-EEG — `bidseeg.py` + channels / events / eeg.json
- XDF (LSL on disk) — `xdfocc.py` + `sub-01_task-spike.xdf`
- BrainVision — `bvocc.py` + `.vhdr` / `.vmrk` / `.eeg`
- WFDB — `wfdbocc.py` + `.hea` / `.dat`
- GDF 1.25 — `gdfocc.py` + `sub-01_task-spike.gdf` / `tape.gdf`
- Public tapes — `resources/DATASETS.md` (PhysioNet, OpenNeuro, BNCI, TUH)

Empty EDF / header-only BIDS / 0-stream XDF / 0-channel BrainVision / 0-signal WFDB refuse. See `resources/FORMATS.md`.

## Show

NumPy on the same spike bins. Their empty `mean` is `nan`. This
kernel refuses. See `SHOW.md`.

## Kernels

- `nyqst.py` — sample occupancy
- `edfocc.py` — EDF occupancy
- `bidseeg.py` — BIDS-EEG occupancy
- `xdfocc.py` — XDF occupancy
- `bvocc.py` — BrainVision occupancy
- `wfdbocc.py` — WFDB occupancy
- `gdfocc.py` — GDF 1.25 occupancy

## Evidence

Pinned `python3.12 nyquist_bench.py`. Numbers are copied from `results/NYQUIST_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_steps | 200000 |
| n_paired | 7 |
| `nyquist` median | 0.011677542002871633 s |
| `len` median | 1.249951310455799e-06 s |
| occupancy (twice) | 200000 |
| EDF samples (twice) | 8 |
| EDF bytes | 528 |
| BIDS occupancy | 2 |
| XDF streams | 1 |
| BrainVision samples | 8 |
| WFDB samples | 8 |

## License

MIT
