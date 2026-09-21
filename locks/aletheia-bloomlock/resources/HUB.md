# Playable BCI files

This kernel now **ingests** a BIDS-EEG events tape in
`resources/synthetic/tape_events.tsv` (keys `[1,2,3]`, maybe-membership 1).
An empty events table refuses.

```bash
python3.12 show_bids.py
```
