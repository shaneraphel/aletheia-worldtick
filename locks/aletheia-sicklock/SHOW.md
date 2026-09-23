# Show: NumPy (an empty sick set)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on five children:
four infection orders, plus a refusal when the sick set is empty.

NumPy 2.4.6 `sum` on an empty array is 0.0.
`infection_sequences(5, [])` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.

# Show: BioSig GDF 1.25 (an empty sick set)

`tape.gdf` holds five channels, sick at 0 and 4. Infection orders are 4.
An empty GDF raises.

```bash
python3.12 show_gdf.py
```

Pinned output: `results/SHOW_GDF.json`.

# Show: official MNE on the five-channel GDF tape

MNE reads `tape.gdf` after the field-major header, and reads EDF+ TAL
`go`/`end` as annotations. Infection orders are 4.
Official empty annotations are 0 descriptions.
An empty GDF raises.

```bash
python3.12 show_mne.py
```

Pinned output: `results/SHOW_MNE.json`.

# Show: MNE BrainVision and edfio on the sick tape

Official MNE reads `tape.vhdr` and `.vmrk` Stimulus `go`/`end`. edfio reads `tape.edf`. Infection orders are 4.

```bash
python3.12 show_brainvision_mne.py
python3.12 show_edfio.py
```

Pinned output: `results/SHOW_BRAINVISION_MNE.json`, `results/SHOW_EDFIO.json`.

# Show: PhysioNet wfdb on the sick tape

Official wfdb reads five format-16 samples and `.atr` NOTE aux_note `go`/`end` at 1.0/2.0 s. Infection orders are 4.

```bash
python3.12 show_wfdb_official.py
```

Pinned output: `results/SHOW_WFDB.json`.

# Show: Lab Streaming Layer XDF

Official pyxdf reads StreamHeader plus Samples and reports `n_streams` 10
(EEG, markers, Accel, Gyro, Orient, Mag, CAN, CanId, Wheel). This kernel reads those samples. An empty
XDF raises.

```bash
python3.12 show_xdf.py
python3.12 show_bids.py
```

Pinned output: `results/SHOW_XDF.json`, `results/SHOW_BIDS.json`.

# Show: MNE on an EEGLAB set (empty events)

Official MNE 1.9.0 reads `tape.set` `EEG.event` `go`/`end` as annotations
at onset 1.0/2.0. Infection orders are 4. An empty `.set` or empty event list raises here.

```bash
python3.12 show_eeglab.py
```

Pinned output: `results/SHOW_EEGLAB.json`.

# Show: MNE and edfio on a BDF tape (empty annotations)

Official MNE `read_raw_bdf` and edfio `read_bdf` read `tape.bdf` and
`BDF Annotations` `go`/`end` at 1.0/2.0 s. Infection orders are 4. An empty
`.bdf` or empty annotation list raises here.

```bash
python3.12 show_bdf.py
```

Pinned output: `results/SHOW_BDF.json`.

# Show: MNE on a Neuroscan CNT tape (empty events)

Official MNE `read_raw_cnt` reads `tape.cnt` and EVENT1 stim `1`/`2` at
1.0/2.0 s. Infection orders are 4. An empty `.cnt` or empty event list raises here.

```bash
python3.12 show_cnt.py
```

Pinned output: `results/SHOW_CNT.json`.

# Show: MNE on a Persyst tape (empty comments)

Official MNE `read_raw_persyst` reads `tape_persyst.lay` and Comments
`go`/`end` at 1.0/2.0 s. Infection orders are 4. An empty `.lay` or empty
comment list raises here.

```bash
python3.12 show_persyst.py
```

Pinned output: `results/SHOW_PERSYST.json`.

# Show: MNE on a Blackrock NSX tape (an empty recording)

Official MNE `read_raw_nsx` reads `tape.ns3`. Infection orders are 4. An empty
`.ns3` raises here.

```bash
python3.12 show_nsx.py
```

Pinned output: `results/SHOW_NSX.json`.

# Show: MNE on a Nicolet tape (an empty recording)

Official MNE `read_raw_nicolet` reads `tape_nicolet.data`. Infection orders are 4.
An empty `.data` raises here. Nicolet has no comment channel.

```bash
python3.12 show_nicolet.py
```

Pinned output: `results/SHOW_NICOLET.json`.

# Show: MNE on a Nihon Kohden tape (empty logs)

Official MNE `read_raw_nihon` reads `tape_nihon.EEG` and LOG `go`/`end`
at 1.0/2.0 s. Infection orders are 4. An empty `.EEG` or empty log list raises here.

```bash
python3.12 show_nihon.py
```

Pinned output: `results/SHOW_NIHON.json`.

# Show: MNE on an EyeLink tape (empty messages)

Official MNE `read_raw_eyelink` reads `tape.asc` and MSG `go`/`end` at 1.0/2.0 s.
Infection orders are 4. An empty `.asc` or empty message list raises here.

```bash
python3.12 show_eyelink.py
```

Pinned output: `results/SHOW_EYELINK.json`.

# Show: MNE on an Eximia tape (an empty recording)

Official MNE `read_raw_eximia` reads `tape.nxe` (5 samples on Cz at 1450 Hz).
Infection orders are 4. An empty `.nxe` raises here.

```bash
python3.12 show_eximia.py
```

Pinned output: `results/SHOW_EXIMIA.json`.

# Show: I fixed the MNE import, then used MNE on an Eximia tape

MNE 1.9.0 imports `sph_harm` from SciPy. SciPy 1.17.1 has no `sph_harm`.
A 6-line shim maps it to `sph_harm_y` (microseconds, numerics match).
Then official `read_raw_eximia` reads `tape.nxe` (5 samples on Cz).
An empty `.nxe` raises here.

```bash
python3.12 show_sph_harm.py
```

Pinned output: `results/SHOW_SPH_HARM.json`.

# Show: MNE on a NIRx tape (an empty recording)

Official MNE 1.9.0 `read_raw_nirx` reads `tape_nirx` (5 samples on S1_D1) and stim `1.0`/`2.0` at 1.0/2.0 s.
An empty NIRx folder or empty event list raises here.

```bash
python3.12 show_nirx.py
```

Pinned output: `results/SHOW_NIRX.json`.

# Show: MNE on a Hitachi tape (an empty recording)

Official MNE 1.9.0 `read_raw_hitachi` reads `tape_hitachi.csv` (5 samples on S1_D1 695). An empty Hitachi CSV raises here.

```bash
python3.12 show_hitachi.py
```

Pinned output: `results/SHOW_HITACHI.json`.

# Show: MNE on a SNIRF tape (an empty recording)

Official MNE 1.9.0 `read_raw_snirf` reads `tape.snirf` (5 samples on S1_D1) and stim `1.0`/`2.0` at 1.0/2.0 s.
An empty SNIRF file or empty stim list raises here.

```bash
python3.12 show_snirf.py
```

Pinned output: `results/SHOW_SNIRF.json`.

# Show: MNE on a BOXY tape (an empty recording)

Official MNE 1.9.0 `read_raw_boxy` reads `tape.boxy` (5 samples on S1_D1 DC) and stim `1.0`/`2.0` at 1.0/2.0 s.
An empty BOXY file or empty marker list raises here.

```bash
python3.12 show_boxy.py
```

Pinned output: `results/SHOW_BOXY.json`.

# Show: MNE on a Curry tape (an empty recording)

Official MNE 1.9.0 `read_raw_curry` reads `tape_curry.dap` (5 samples on Cz) and event `1`/`2` at 1.0/2.0 s.
An empty Curry set or empty event list raises here.

```bash
python3.12 show_curry.py
```

Pinned output: `results/SHOW_CURRY.json`.

# Show: MNE on an EGI tape (an empty recording)

Official MNE 1.9.0 `read_raw_egi` reads `tape_egi.raw` (5 samples on E1) and `DIN1`/`DIN2` at 1.0/2.0 s.
An empty EGI file or empty event list raises here.

```bash
python3.12 show_egi.py
```

Pinned output: `results/SHOW_EGI.json`.
