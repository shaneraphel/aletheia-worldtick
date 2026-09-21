# Synthetic BCI tape (MIT)

One channel, eight samples `[1, 2, 3, -1, 2, 0, 4, 5]`.

- `sub-01_task-spike_eeg.edf` — EDF+C with `EDF Annotations` TAL `go`/`end`
- `sub-01_task-spike_eeg.bdf` — BDF+C 24-bit with `BDF Annotations` TAL `go`/`end`
- `sub-01_task-spike_channels.tsv` / `_events.tsv` / `_marker_events.tsv` / `_annotations.txt` / `_eeg.json` — BIDS-EEG plus XDF string markers and official MNE annotations
- `dataset_description.json` — BIDS dataset card
- `sub-01_task-spike.xdf` — XDF FileHeader + StreamHeader + Samples, stream count 1
- `sub-01_task-spike.vhdr` / `.vmrk` / `.eeg` — BrainVision 1.0 with Stimulus `go`/`end`
- `sub-01_task-spike.hea` / `.dat` / `.atr` — WFDB format 16 plus NOTE aux_note `go`/`end`
- `sub-01_task-spike.cnt` — Neuroscan CNT with EVENT1 stim `1`/`2`
- `sub-01_task-spike_persyst.lay` / `sub-01_task-spike_persyst.dat` — Persyst FileInfo+Comments `go`/`end`
- `sub-01_task-spike.ns3` — Blackrock NEURALCD 2.2 int16 on Cz
- `sub-01_task-spike_nicolet.head` / `sub-01_task-spike_nicolet.data` — Nicolet ASCII header + int16
- `sub-01_task-spike_nihon.EEG` / `.PNT` / `.LOG` — Nihon Kohden waveform plus LOG `go`/`end`
- `sub-01_task-spike.asc` — EyeLink gaze ASCII with MSG `go`/`end`
- `sub-01_task-spike.nxe` — Eximia 64ch int16 with Cz tape
- `sub-01_task-spike_nirx/` — NIRx NIRStar 15.3 folder with wl1 tape and evt 1/2
- `sub-01_task-spike_hitachi.csv` — Hitachi ETG-7000 3x5 CSV with CH1 tape
- `sub-01_task-spike.snirf` — SNIRF HDF5 with S1_D1 tape and stim 1.0/2.0
- `sub-01_task-spike.boxy` — ISS Imagent BOXY 0.84 parsed with A-DC1 tape and digaux 1/2
- `sub-01_task-spike_curry.dap` / `.dat` / `.rs3` / `.cef` — Curry 7 ASCII with Cz tape and event 1/2
- `sub-01_task-spike_egi.raw` — EGI simple binary with E1 tape and DIN1/DIN2
