# Show: I used pyahocorasick, and I refused the empty needle

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [WojciechMula/pyahocorasick](https://github.com/WojciechMula/pyahocorasick)
on a token tape: overlapping needles `ab` and `bc` in `abcabc`, plus a refusal
when the text or a pattern is empty.

`add_word("")` is accepted there. `aho_hits` refuses an empty tape. The note
on their tree is
[WojciechMula/pyahocorasick#225](https://github.com/WojciechMula/pyahocorasick/issues/225).

```bash
python3.12 show_ahocorasick.py
```

Pinned output: `results/SHOW_AHOCORASICK.json`.
