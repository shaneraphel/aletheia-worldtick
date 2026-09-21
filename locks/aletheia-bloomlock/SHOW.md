# Show: I used pybloom-live, and I refused the empty filter

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [joseph-fox/python-bloomfilter](https://github.com/joseph-fox/python-bloomfilter)
on a three-key spike filter: the same maybe-membership 1, plus a refusal when
the key tape is empty.

pybloom-live 4.0.0 membership of `2` on a filter with no keys is `False`.
`bloom_maybe([], 16, 2, 2)` raises.

```bash
python3.12 show_pybloom.py
```

Pinned output: `results/SHOW_PYBLOOM.json`.

# Show: I used BioSig GDF 1.25, and I refused an empty recording

`tape.gdf` holds onsets `[1,2,3]`. Maybe-membership is 1. An empty GDF raises.

```bash
python3.12 show_gdf.py
```

Pinned output: `results/SHOW_GDF.json`.

# Show: I used official MNE and edfio on the same onsets

MNE reads `tape.gdf` and EDF+ TAL `go`/`end` as annotations.
edfio reads `tape.edf`. Maybe-membership is 1. Official empty
annotations are 0 descriptions.

```bash
python3.12 show_mne.py
python3.12 show_edfio.py
```

Pinned output: `results/SHOW_MNE.json`, `results/SHOW_EDFIO.json`.

# Show: I used MNE on BrainVision

Official MNE reads `tape.vhdr` and `.vmrk` Stimulus `go`/`end`. Maybe-membership is 1. An empty `.vhdr` raises.

```bash
python3.12 show_brainvision_mne.py
```

Pinned output: `results/SHOW_BRAINVISION_MNE.json`.

# Show: I used PhysioNet wfdb on the key tape

Official wfdb reads `tape.hea` / `tape.dat` and `.atr` NOTE aux_note `go`/`end` at 1.0/2.0 s. Maybe-membership is 1.

```bash
python3.12 show_wfdb_official.py
```

Pinned output: `results/SHOW_WFDB.json`.

# Show: I used Lab Streaming Layer XDF

Official pyxdf reads StreamHeader plus Samples and reports `n_streams` 10
(EEG, markers, Accel, Gyro, Orient, Mag, CAN, CanId, Wheel). This kernel reads those samples. An empty
XDF raises.

```bash
python3.12 show_xdf.py
python3.12 show_bids.py
```

Pinned output: `results/SHOW_XDF.json`, `results/SHOW_BIDS.json`.

# Show: I used MNE on an EEGLAB set, and I refused empty events

Official MNE 1.9.0 reads `tape.set` `EEG.event` `go`/`end` as annotations
at onset 1.0/2.0. Maybe-membership is 1. An empty `.set` or empty event list raises here.

```bash
python3.12 show_eeglab.py
```

Pinned output: `results/SHOW_EEGLAB.json`.

# Show: I used MNE and edfio on a BDF tape, and I refused empty annotations

Official MNE `read_raw_bdf` and edfio `read_bdf` read `tape.bdf` and
`BDF Annotations` `go`/`end` at 1.0/2.0 s. Maybe-membership is 1. An empty
`.bdf` or empty annotation list raises here.

```bash
python3.12 show_bdf.py
```

Pinned output: `results/SHOW_BDF.json`.

# Show: I used MNE on a Neuroscan CNT tape, and I refused empty events

Official MNE `read_raw_cnt` reads `tape.cnt` and EVENT1 stim `1`/`2` at
1.0/2.0 s. Maybe-membership is 1. An empty `.cnt` or empty event list raises here.

```bash
python3.12 show_cnt.py
```

Pinned output: `results/SHOW_CNT.json`.

# Show: I used MNE on a Persyst tape, and I refused empty comments

Official MNE `read_raw_persyst` reads `tape_persyst.lay` and Comments
`go`/`end` at 1.0/2.0 s. Maybe-membership is 1. An empty `.lay` or empty
comment list raises here.

```bash
python3.12 show_persyst.py
```

Pinned output: `results/SHOW_PERSYST.json`.

# Show: I used MNE on a Blackrock NSX tape, and I refused an empty recording

Official MNE `read_raw_nsx` reads `tape.ns3`. Maybe-membership is 1. An empty
`.ns3` raises here.

```bash
python3.12 show_nsx.py
```

Pinned output: `results/SHOW_NSX.json`.

# Show: I used MNE on a Nicolet tape, and I refused an empty recording

Official MNE `read_raw_nicolet` reads `tape_nicolet.data`. Maybe-membership is 1.
An empty `.data` raises here. Nicolet has no comment channel.

```bash
python3.12 show_nicolet.py
```

Pinned output: `results/SHOW_NICOLET.json`.

# Show: I used MNE on a Nihon Kohden tape, and I refused empty logs

Official MNE `read_raw_nihon` reads `tape_nihon.EEG` and LOG `go`/`end`
at 1.0/2.0 s. Maybe-membership is 1. An empty `.EEG` or empty log list raises here.

```bash
python3.12 show_nihon.py
```

Pinned output: `results/SHOW_NIHON.json`.

# Show: I used MNE on an EyeLink tape, and I refused empty messages

Official MNE `read_raw_eyelink` reads `tape.asc` and MSG `go`/`end` at 1.0/2.0 s.
Maybe-membership is 1. An empty `.asc` or empty message list raises here.

```bash
python3.12 show_eyelink.py
```

Pinned output: `results/SHOW_EYELINK.json`.

# Show: I used MNE on an Eximia tape, and I refused an empty recording

Official MNE `read_raw_eximia` reads `tape.nxe` (3 samples on Cz at 1450 Hz).
Maybe-membership is 1. An empty `.nxe` raises here.

```bash
python3.12 show_eximia.py
```

Pinned output: `results/SHOW_EXIMIA.json`.

# Show: I fixed the MNE import, then used MNE on an Eximia tape

MNE 1.9.0 imports `sph_harm` from SciPy. SciPy 1.17.1 has no `sph_harm`.
A 6-line shim maps it to `sph_harm_y` (microseconds, numerics match).
Then official `read_raw_eximia` reads `tape.nxe` (3 samples on Cz).
An empty `.nxe` raises here.

```bash
python3.12 show_sph_harm.py
```

Pinned output: `results/SHOW_SPH_HARM.json`.

# Show: I used MNE on a NIRx tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_nirx` reads `tape_nirx` (3 samples on S1_D1) and stim `1.0`/`2.0` at 1.0/2.0 s.
An empty NIRx folder or empty event list raises here.

```bash
python3.12 show_nirx.py
```

Pinned output: `results/SHOW_NIRX.json`.

# Show: I used MNE on a Hitachi tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_hitachi` reads `tape_hitachi.csv` (3 samples on S1_D1 695). An empty Hitachi CSV raises here.

```bash
python3.12 show_hitachi.py
```

Pinned output: `results/SHOW_HITACHI.json`.

# Show: I used MNE on a SNIRF tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_snirf` reads `tape.snirf` (3 samples on S1_D1) and stim `1.0`/`2.0` at 1.0/2.0 s.
An empty SNIRF file or empty stim list raises here.

```bash
python3.12 show_snirf.py
```

Pinned output: `results/SHOW_SNIRF.json`.

# Show: I used MNE on a BOXY tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_boxy` reads `tape.boxy` (3 samples on S1_D1 DC) and stim `1.0`/`2.0` at 1.0/2.0 s.
An empty BOXY file or empty marker list raises here.

```bash
python3.12 show_boxy.py
```

Pinned output: `results/SHOW_BOXY.json`.

# Show: I used MNE on a Curry tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_curry` reads `tape_curry.dap` (3 samples on Cz) and event `1`/`2` at 1.0/2.0 s.
An empty Curry set or empty event list raises here.

```bash
python3.12 show_curry.py
```

Pinned output: `results/SHOW_CURRY.json`.

# Show: I used MNE on an EGI tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_egi` reads `tape_egi.raw` (3 samples on E1) and `DIN1`/`DIN2` at 1.0/2.0 s.
An empty EGI file or empty event list raises here.

```bash
python3.12 show_egi.py
```

Pinned output: `results/SHOW_EGI.json`.
