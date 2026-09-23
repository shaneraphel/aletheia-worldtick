# Show: pyahocorasick (the empty text tape)

Compared with [WojciechMula/pyahocorasick](https://github.com/WojciechMula/pyahocorasick)
on `aba`: suffix-link occupancy 3, plus a refusal when the text is empty.

pyahocorasick 2.3.1 empty `add_word` is accepted.
`n_suffix_links("")` raises.

```bash
python3.12 show_ahocorasick.py
```

Pinned output: `results/SHOW_AHOCORASICK.json`.
