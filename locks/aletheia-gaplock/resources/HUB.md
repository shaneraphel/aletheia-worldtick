# Playable BCI files

This kernel now **ingests** a BIDS-EEG events tape in
`resources/synthetic/tape_events.tsv` (blooms `[1,3,2]`, day 2).
An empty events table refuses.

```bash
python3.12 show_bids.py
```
