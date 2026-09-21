# Playable BCI files

This kernel now **ingests** a BIDS-EEG events tape in
`resources/synthetic/tape_events.tsv` (`trial_type` `aba`, 3 suffix links).
An empty events table refuses.

```bash
python3.12 show_bids.py
```
