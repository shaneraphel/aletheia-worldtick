# Show: I used NumPy, and I refused the empty spike tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [numpy/numpy](https://github.com/numpy/numpy) on a three-bin
recording: occupancy 3 here, plus a refusal when the tape is empty.

NumPy 2.4.6 `mean` on an empty array is `nan`.
`nyquist([])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.

# Show: I used PhysioNet EDF, and I refused an empty recording

This repo is also what I built with the PhysioNet EEG interchange
([eegmmidb](https://physionet.org/content/eegmmidb/)): one MIT EDF of our own
(8 samples on `EEG Cz`), BIDS-EEG sidecars, and one XDF stream.

An empty EDF raises. A header-only `channels.tsv` raises. Stream count 0 raises.

```bash
python3.12 show_edf.py
```

Pinned output: `results/SHOW_EDF.json`.

# Show: I used BioSig GDF 1.25, and I refused an empty recording

This repo ships a GDF 1.25 writer. Official
[MNE-Python](https://github.com/mne-tools/mne-python) 1.9.0 reads the same
8-sample EDF+ tape and reads BIDS `trial_type` `go`/`end` as EDF TAL
annotations.
Their empty `RawArray` has `n_times=0`. Official empty annotations are
0 descriptions. An empty GDF or empty trial_type raises here.

```bash
python3.12 show_gdf.py
python3.12 show_mne.py
python3.12 show_wfdb_official.py
python3.12 show_edfio.py
```

Pinned output: `results/SHOW_GDF.json`, `results/SHOW_MNE.json`,
`results/SHOW_WFDB.json`, `results/SHOW_EDFIO.json`.

# Show: I used PhysioNet wfdb on the spike tape

Official wfdb 4.3.1 reads `sub-01_task-spike.hea` / `.dat` (8 samples)
and `.atr` NOTE aux_note `go`/`end` at 1.0/2.0 s. An empty header or
empty annotation list raises here.

```bash
python3.12 show_wfdb_official.py
```

Pinned output: `results/SHOW_WFDB.json`.

# Show: I used MNE on BrainVision, and I refused an empty header

Official MNE 1.9.0 reads `sub-01_task-spike.vhdr` (8 samples) and
`.vmrk` Stimulus `go`/`end` as annotations. An empty `.vhdr` or empty
marker list raises here. FIF stays with MNE; it is not rewritten.

```bash
python3.12 show_brainvision_mne.py
```

Pinned output: `results/SHOW_BRAINVISION_MNE.json`.

# Show: I used Lab Streaming Layer XDF StreamHeader + Samples

Official pyxdf 1.17.5 reads StreamHeader plus Samples and reports
`n_streams` 10 on `sub-01_task-spike.xdf` (EEG, string markers `go`/`end`, float32 Accel, float32 Gyro, float32 Orient, float32 Mag, float32 CAN, int16 CanId, float32 Wheel, float32 Pedal).
Those eight digital samples match the EDF tape. An empty XDF raises.

```bash
python3.12 show_xdf.py
```

Pinned output: `results/SHOW_XDF.json`.

# Show: I used MNE on an EEGLAB set, and I refused empty events

Official MNE 1.9.0 reads `tape.set` `EEG.event` `go`/`end` as annotations
at onset 1.0/2.0. An empty `.set` or empty event list raises here.

```bash
python3.12 show_eeglab.py
```

Pinned output: `results/SHOW_EEGLAB.json`.

# Show: I used MNE and edfio on a BDF tape, and I refused empty annotations

Official MNE 1.9.0 `read_raw_bdf` and edfio 0.4.16 `read_bdf` read
`sub-01_task-spike_eeg.bdf` (8 samples, `\xffBIOSEMI`) and
`BDF Annotations` `go`/`end` at 1.0/2.0 s. An empty `.bdf` or empty
annotation list raises here.

```bash
python3.12 show_bdf.py
```

Pinned output: `results/SHOW_BDF.json`.

# Show: I used MNE on a Neuroscan CNT tape, and I refused empty events

Official MNE 1.9.0 `read_raw_cnt` reads `sub-01_task-spike.cnt` (8 samples)
and EVENT1 stim `1`/`2` at 1.0/2.0 s. An empty `.cnt` or empty event list
raises here. ANT Neuro CNT stays with MNE; it is not rewritten.

```bash
python3.12 show_cnt.py
```

Pinned output: `results/SHOW_CNT.json`.

# Show: I used MNE on a Persyst tape, and I refused empty comments

Official MNE 1.9.0 `read_raw_persyst` reads `sub-01_task-spike_persyst.lay`
(8 samples) and Comments `go`/`end` at 1.0/2.0 s. An empty `.lay` raises here.
Official empty Comments are 0 descriptions; ours empty comments raise.
ANT Neuro CNT stays with MNE; it is not rewritten.

```bash
python3.12 show_persyst.py
```

Pinned output: `results/SHOW_PERSYST.json`.

# Show: I used MNE on a Blackrock NSX tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_nsx` reads `sub-01_task-spike.ns3` (8 samples on Cz).
An empty `.ns3` raises here. NSX comments are acquisition skips, not `trial_type`.

```bash
python3.12 show_nsx.py
```

Pinned output: `results/SHOW_NSX.json`.

# Show: I used MNE on a Nicolet tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_nicolet` reads `sub-01_task-spike_nicolet.data` (8 samples on Cz).
An empty `.data` raises here. Nicolet has no comment channel.

```bash
python3.12 show_nicolet.py
```

Pinned output: `results/SHOW_NICOLET.json`.

# Show: I used MNE on a Nihon Kohden tape, and I refused empty logs

Official MNE 1.9.0 `read_raw_nihon` reads `sub-01_task-spike_nihon.EEG`
(8 samples on C3) and LOG `go`/`end` at 1.0/2.0 s. An empty `.EEG` raises here.
Official missing LOG is 0 descriptions; ours empty logs raise.

```bash
python3.12 show_nihon.py
```

Pinned output: `results/SHOW_NIHON.json`.

# Show: I used MNE on an EyeLink tape, and I refused empty messages

Official MNE 1.9.0 `read_raw_eyelink` reads `sub-01_task-spike.asc` (8 pupil
samples) and MSG `go`/`end` at 1.0/2.0 s. An empty `.asc` or empty message list
raises here.

```bash
python3.12 show_eyelink.py
```

Pinned output: `results/SHOW_EYELINK.json`.

# Show: I used MNE on an Eximia tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_eximia` reads `sub-01_task-spike.nxe` (8 samples
on Cz at 1450 Hz). An empty `.nxe` raises here. Eximia has no comment channel.

```bash
python3.12 show_eximia.py
```

Pinned output: `results/SHOW_EXIMIA.json`.

# Show: I fixed the MNE import, then used MNE on an Eximia tape

MNE 1.9.0 imports `sph_harm` from SciPy. SciPy 1.17.1 has no `sph_harm`.
A 6-line shim maps it to `sph_harm_y` (1.7 microseconds, numerics match).
Then official `read_raw_eximia` reads `sub-01_task-spike.nxe` (8 samples on Cz).
An empty `.nxe` raises here.

```bash
python3.12 show_sph_harm.py
```

Pinned output: `results/SHOW_SPH_HARM.json`.

# Show: I used MNE on a NIRx tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_nirx` reads `sub-01_task-spike_nirx` (8 samples on S1_D1) and stim `1.0`/`2.0` at 1.0/2.0 s.
An empty NIRx folder or empty event list raises here.

```bash
python3.12 show_nirx.py
```

Pinned output: `results/SHOW_NIRX.json`.

# Show: I used MNE on a Hitachi tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_hitachi` reads `sub-01_task-spike_hitachi.csv` (8 samples on S1_D1 695). An empty Hitachi CSV raises here.

```bash
python3.12 show_hitachi.py
```

Pinned output: `results/SHOW_HITACHI.json`.

# Show: I used MNE on a SNIRF tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_snirf` reads `sub-01_task-spike.snirf` (8 samples on S1_D1) and stim `1.0`/`2.0` at 1.0/2.0 s.
An empty SNIRF file or empty stim list raises here.

```bash
python3.12 show_snirf.py
```

Pinned output: `results/SHOW_SNIRF.json`.

# Show: I used MNE on a BOXY tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_boxy` reads `sub-01_task-spike.boxy` (8 samples on S1_D1 DC) and stim `1.0`/`2.0` at 1.0/2.0 s.
An empty BOXY file or empty marker list raises here.

```bash
python3.12 show_boxy.py
```

Pinned output: `results/SHOW_BOXY.json`.

# Show: I used MNE on a Curry tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_curry` reads `sub-01_task-spike_curry.dap` (8 samples on Cz) and event `1`/`2` at 1.0/2.0 s.
An empty Curry set or empty event list raises here.

```bash
python3.12 show_curry.py
```

Pinned output: `results/SHOW_CURRY.json`.

# Show: I used MNE on an EGI tape, and I refused an empty recording

Official MNE 1.9.0 `read_raw_egi` reads `sub-01_task-spike_egi.raw` (8 samples on E1) and `DIN1`/`DIN2` at 1.0/2.0 s.
An empty EGI file or empty event list raises here.

```bash
python3.12 show_egi.py
```

Pinned output: `results/SHOW_EGI.json`.
