# What a BCI resource is

NeuroTechX [awesome-bci](https://github.com/NeuroTechX/awesome-bci) lists
software that **reads a recording**, **writes a recording**, or **names a
public tape**. Hardware and papers sit in other sections. A kernel that only
counts integers is not yet a BCI resource.

The missing pieces on these occupancy repos were the interchange formats:

| format | what it is | empty case |
|---|---|---|
| **EDF / EDF+ / BDF** | PhysioNet and OpenNeuro EEG interchange; EDF+ TAL and BDF+C `BDF Annotations` copy `trial_type` | 0 channels is absence; empty TAL is absence |
| **BIDS-EEG** | `channels.tsv` + `events.tsv` + `eeg.json` beside the EDF | header-only tables are absence |
| **MNE annotations** | BIDS `trial_type` copied into official `.txt` `description` | official empty `.txt` is 0; ours empty is absence |
| **XDF** | on-disk [Lab Streaming Layer](https://github.com/sccn/labstreaminglayer) | 0 streams is absence |
| **FIF** | MNE / Elekta native | provided by MNE, not re-emitted here |
| **EEGLAB .set** | MATLAB v5 EEG struct via SciPy `savemat`; `EEG.event` type+latency copies `trial_type` | 0 pnts is absence; empty events are absence |
| **WFDB** | PhysioNet `.hea` / `.dat` format 16; `.atr` NOTE aux_note copies `trial_type` | 0 signals is absence; empty `.atr` is absence |
| **Neuroscan CNT** | 900-byte SETUP + ELECTLOC + int16; EVENT1 stim codes | 0 channels is absence; empty events are absence |
| **Persyst .lay/.dat** | ASCII FileInfo+ChannelMap+Comments; comment text copies `trial_type` | 0 channels is absence; empty comments are absence |
| **Blackrock NSX** | NEURALCD 2.2 `.ns3` int16 packets; Utah-array / iBCI interchange | 0 channels is absence |
| **Nicolet** | ASCII `.head` `key=value` + int16 `.data` | 0 channels is absence |
| **Nihon Kohden** | `.EEG` + `.PNT` clock + `.LOG` trial labels copy `trial_type` | 0 channels is absence; empty LOG is absence |
| **EyeLink .asc** | SR Research gaze START/SAMPLES/MSG; MSG copies `trial_type` | 0 samples is absence; empty MSG is absence |
| **Eximia .nxe** | TMS-EEG 64ch int16 multiplexed; Cz carries the tape | 0 samples is absence |
| **NIRx NIRStar** | fNIRS folder hdr/inf/wl1/wl2/evt; stim bits copy numeric descriptions | 0 samples is absence; empty evt is absence |
| **Hitachi ETG CSV** | fNIRS ETG-7000 3x5 optical CSV; CH1 carries the tape | 0 samples is absence |
| **SNIRF** | fNIRS HDF5 interchange; stim names copy numeric descriptions | 0 samples is absence; empty stim is absence |
| **ISS BOXY** | optical imaging 0.84 parsed `A-DC1` plus `digaux` markers | 0 samples is absence; empty digaux is absence |
| **Curry 7** | Neuroscan Curry `.dap`/`.dat`/`.rs3` plus `.cef` event codes | 0 samples is absence; empty cef is absence |
| **EGI simple binary** | Net Station int16 plus named DIN event codes | 0 samples is absence; empty DIN is absence |
| **GDF 1.25** | BioSig 1.x header + int16 samples | 0 channels is absence |

Playable files live in `resources/synthetic/`. The occupancy kernels are
`edfocc.py`, `bidseeg.py`, `xdfocc.py`, and `persystocc.py`, `nsxocc.py`, `nicoletocc.py`, `nihonocc.py`, `eyelinkocc.py`, `eximiaocc.py`, `nirxocc.py`, `hitachiocc.py`, `snirfocc.py`, `boxyocc.py`, `curryocc.py`, `egiocc.py`. An empty tape raises.

```bash
python3.12 edfocc_bench.py
python3.12 show_edf.py
python3.12 show_persyst.py
python3.12 show_nsx.py
python3.12 show_nicolet.py
python3.12 show_nihon.py
python3.12 show_eyelink.py
python3.12 show_eximia.py
python3.12 show_eeglab.py
python3.12 show_gdf.py
```
