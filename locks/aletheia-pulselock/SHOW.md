# Show: NumPy (an empty pulse tape)

Compared with [numpy/numpy](https://github.com/numpy/numpy) on five pulses:
strength 22 for k=3, plus a refusal when the tape is empty.

NumPy 2.4.6 `sum` on an empty array is 0.0.
`max_k_subarray_strength([], 1)` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.

# Show: BioSig GDF 1.25 (an empty pulse tape)

`pulse.gdf` holds `[1,2,3,-1,2]`. Strength is 22. Official MNE 1.9.0 reads
the same five GDF samples and reads EDF+ TAL `go`/`end` as
annotations. Official empty annotations are 0 descriptions. An empty
GDF or empty TAL raises.

```bash
python3.12 show_gdf.py
python3.12 show_mne.py
```

Pinned output: `results/SHOW_GDF.json`, `results/SHOW_MNE.json`.

# Show: edfio and MNE BrainVision on the pulse tape

edfio reads `tape_eeg.edf`. Official MNE reads `pulse.vhdr` and `.vmrk` Stimulus `go`/`end`. Strength is 22.
An empty EDF or empty `.vhdr` raises.

```bash
python3.12 show_edfio.py
python3.12 show_brainvision_mne.py
```

Pinned output: `results/SHOW_EDFIO.json`, `results/SHOW_BRAINVISION_MNE.json`.

# Show: PhysioNet wfdb on the pulse tape

Official wfdb reads `pulse.hea` / `pulse.dat` (signal line names `pulse.dat`)
and `.atr` NOTE aux_note `go`/`end` at 1.0/2.0 s.
Strength is 22. An empty header or empty annotation list raises.

```bash
python3.12 show_wfdb_official.py
```

Pinned output: `results/SHOW_WFDB.json`.

# Show: XDF and BIDS-EEG on the pulse tape

Official pyxdf 1.17.5 reads StreamHeader plus Samples and reports
`n_streams` 10 (EEG, string markers `go`/`end`, float32 Accel, float32 Gyro, float32 Orient, float32 Mag, float32 CAN, int16 CanId, float32 Wheel, float32 Pedal). This kernel occupies those
samples `[1,2,3,-1,2]`. Strength is 22. Empty XDF and header-only
BIDS events raise.

```bash
python3.12 show_xdf.py
python3.12 show_bids.py
```

Pinned output: `results/SHOW_XDF.json`, `results/SHOW_BIDS.json`.

# Show: MNE on an EEGLAB set (empty events)

Official MNE 1.9.0 reads `pulse.set` `EEG.event` `go`/`end` as annotations
at onset 1.0/2.0. Strength is 22. An empty `.set` or empty event list raises here.

```bash
python3.12 show_eeglab.py
```

Pinned output: `results/SHOW_EEGLAB.json`.

# Show: MNE and edfio on a BDF tape (empty annotations)

Official MNE `read_raw_bdf` and edfio `read_bdf` read `tape_eeg.bdf`
and `BDF Annotations` `go`/`end` at 1.0/2.0 s. Strength is 22. An empty
`.bdf` or empty annotation list raises here.

```bash
python3.12 show_bdf.py
```

Pinned output: `results/SHOW_BDF.json`.

# Show: MNE on a Neuroscan CNT tape (empty events)

Official MNE `read_raw_cnt` reads `pulse.cnt` and EVENT1 stim `1`/`2` at
1.0/2.0 s. Strength is 22. An empty `.cnt` or empty event list raises here.

```bash
python3.12 show_cnt.py
```

Pinned output: `results/SHOW_CNT.json`.

# Show: MNE on a Persyst tape (empty comments)

Official MNE `read_raw_persyst` reads `pulse_persyst.lay` and Comments
`go`/`end` at 1.0/2.0 s. Strength is 22. An empty `.lay` or empty comment
list raises here.

```bash
python3.12 show_persyst.py
```

Pinned output: `results/SHOW_PERSYST.json`.

# Show: MNE on a Blackrock NSX tape (an empty recording)

Official MNE `read_raw_nsx` reads `pulse.ns3`. Strength is 22. An empty `.ns3`
raises here.

```bash
python3.12 show_nsx.py
```

Pinned output: `results/SHOW_NSX.json`.

# Show: MNE on a Nicolet tape (an empty recording)

Official MNE `read_raw_nicolet` reads `pulse_nicolet.data`. Strength is 22.
An empty `.data` raises here. Nicolet has no comment channel.

```bash
python3.12 show_nicolet.py
```

Pinned output: `results/SHOW_NICOLET.json`.

# Show: MNE on a Nihon Kohden tape (empty logs)

Official MNE `read_raw_nihon` reads `pulse_nihon.EEG` and LOG `go`/`end`
at 1.0/2.0 s. Strength is 22. An empty `.EEG` or empty log list raises here.

```bash
python3.12 show_nihon.py
```

Pinned output: `results/SHOW_NIHON.json`.

# Show: MNE on an EyeLink tape (empty messages)

Official MNE `read_raw_eyelink` reads `pulse.asc` and MSG `go`/`end` at 1.0/2.0 s.
Strength is 22. An empty `.asc` or empty message list raises here.

```bash
python3.12 show_eyelink.py
```

Pinned output: `results/SHOW_EYELINK.json`.

# Show: MNE on an Eximia tape (an empty recording)

Official MNE `read_raw_eximia` reads `pulse.nxe` (5 samples on Cz at 1450 Hz).
Strength is 22. An empty `.nxe` raises here.

```bash
python3.12 show_eximia.py
```

Pinned output: `results/SHOW_EXIMIA.json`.

# Show: I fixed the MNE import, then used MNE on an Eximia tape

MNE 1.9.0 imports `sph_harm` from SciPy. SciPy 1.17.1 has no `sph_harm`.
A 6-line shim maps it to `sph_harm_y` (microseconds, numerics match).
Then official `read_raw_eximia` reads `pulse.nxe` (5 samples on Cz).
An empty `.nxe` raises here.

```bash
python3.12 show_sph_harm.py
```

Pinned output: `results/SHOW_SPH_HARM.json`.

# Show: MNE on a NIRx tape (an empty recording)

Official MNE 1.9.0 `read_raw_nirx` reads `pulse_nirx` (5 samples on S1_D1) and stim `1.0`/`2.0` at 1.0/2.0 s.
An empty NIRx folder or empty event list raises here.

```bash
python3.12 show_nirx.py
```

Pinned output: `results/SHOW_NIRX.json`.

# Show: MNE on a Hitachi tape (an empty recording)

Official MNE 1.9.0 `read_raw_hitachi` reads `pulse_hitachi.csv` (5 samples on S1_D1 695). An empty Hitachi CSV raises here.

```bash
python3.12 show_hitachi.py
```

Pinned output: `results/SHOW_HITACHI.json`.

# Show: MNE on a SNIRF tape (an empty recording)

Official MNE 1.9.0 `read_raw_snirf` reads `pulse.snirf` (5 samples on S1_D1) and stim `1.0`/`2.0` at 1.0/2.0 s.
An empty SNIRF file or empty stim list raises here.

```bash
python3.12 show_snirf.py
```

Pinned output: `results/SHOW_SNIRF.json`.

# Show: MNE on a BOXY tape (an empty recording)

Official MNE 1.9.0 `read_raw_boxy` reads `pulse.boxy` (5 samples on S1_D1 DC) and stim `1.0`/`2.0` at 1.0/2.0 s.
An empty BOXY file or empty marker list raises here.

```bash
python3.12 show_boxy.py
```

Pinned output: `results/SHOW_BOXY.json`.

# Show: MNE on a Curry tape (an empty recording)

Official MNE 1.9.0 `read_raw_curry` reads `pulse_curry.dap` (5 samples on Cz) and event `1`/`2` at 1.0/2.0 s.
An empty Curry set or empty event list raises here.

```bash
python3.12 show_curry.py
```

Pinned output: `results/SHOW_CURRY.json`.

# Show: MNE on an EGI tape (an empty recording)

Official MNE 1.9.0 `read_raw_egi` reads `pulse_egi.raw` (5 samples on E1) and `DIN1`/`DIN2` at 1.0/2.0 s.
An empty EGI file or empty event list raises here.

```bash
python3.12 show_egi.py
```

Pinned output: `results/SHOW_EGI.json`.
