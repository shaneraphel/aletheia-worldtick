# Show: I used a Python dict, and I refused the empty key tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with the stdlib dict on three keys: the same placed count 3, plus a
refusal when the key tape is empty.

An empty dict `get` is `None`.
`cuckoo_placed([], 5)` raises.

```bash
python3.12 show_dict.py
```

Pinned output: `results/SHOW_DICT.json`.
