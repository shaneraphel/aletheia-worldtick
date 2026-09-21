# Playable BCI files

This kernel now **ingests** an EDF pulse tape in `resources/synthetic/tape_eeg.edf`
(samples `[1,2,3,-1,2]`, strength 22). Empty EDF refuses.

The interchange writers live in
https://github.com/shaneraphel/aletheia-spikelock
(`edfocc.py`, `bidseeg.py`, `xdfocc.py`, `bvocc.py`, `wfdbocc.py`).

```bash
python3.12 show_edf.py
```
