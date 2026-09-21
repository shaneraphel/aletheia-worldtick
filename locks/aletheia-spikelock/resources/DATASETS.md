# Public BCI tapes

These are the databases [awesome-bci](https://github.com/NeuroTechX/awesome-bci)
already names. This repo does not host their bytes. It hosts one MIT EDF of
its own, plus the occupancy kernels that refuse an empty header.

| tape | url | format |
|---|---|---|
| PhysioNet EEG Motor Movement/Imagery | https://physionet.org/content/eegmmidb/ | EDF |
| PhysioNet EEG | https://physionet.org/ | EDF / WFDB |
| OpenNeuro | https://openneuro.org/ | BIDS-EEG (EDF or BrainVision) |
| BNCI Horizon 2020 | https://bnci-horizon-2020.eu/database/data-sets | MAT / GDF |
| Temple University EEG | https://isip.piconepress.com/projects/ | EDF |
| MindBigData | https://mindbigdata.com/opendb/index.html | CSV |
| SCCN public EEG/ERP | https://sccn.ucsd.edu/~arno/fam2data/publicly_available_EEG_data.html | various |
| National Sleep Research Resource | https://sleepdata.org/ | EDF |

The synthetic tape here is `resources/synthetic/sub-01_task-spike_eeg.edf`
(1 channel, 8 samples, EDF 1.0, 528 bytes). BIDS sidecars sit next to it.
XDF is `sub-01_task-spike.xdf`. BrainVision is `.vhdr` / `.vmrk` / `.eeg`.
WFDB is `.hea` / `.dat`. GDF 1.25 is `sub-01_task-spike.gdf` (same 8 samples)
plus `tape.gdf` (3 samples). Official MNE 1.9.0 reads both the EDF and the GDF.
