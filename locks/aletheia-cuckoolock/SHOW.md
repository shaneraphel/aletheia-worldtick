# Show: a Python dict (the empty key tape)

Compared with the stdlib dict on three keys: the same placed count 3, plus a
refusal when the key tape is empty.

An empty dict `get` is `None`.
`cuckoo_placed([], 5)` raises.

```bash
python3.12 show_dict.py
```

Pinned output: `results/SHOW_DICT.json`.
