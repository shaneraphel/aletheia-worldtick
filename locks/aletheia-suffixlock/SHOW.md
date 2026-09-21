# Show: I used pyahocorasick, and I refused the empty text tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [WojciechMula/pyahocorasick](https://github.com/WojciechMula/pyahocorasick)
on `aba`: suffix-link occupancy 3, plus a refusal when the text is empty.

pyahocorasick 2.3.1 empty `add_word` is accepted.
`n_suffix_links("")` raises.

```bash
python3.12 show_ahocorasick.py
```

Pinned output: `results/SHOW_AHOCORASICK.json`.
