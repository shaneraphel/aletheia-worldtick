# Show: intervaltree (the empty slot tape)

Compared with [chaimleib/intervaltree](https://github.com/chaimleib/intervaltree)
on two world-model slots: overlap 2 at time 3, plus a refusal when the
interval tape is empty.

intervaltree 3.2.1 `at(0)` on an empty tree is `[]`.
`interval_tree_overlap([], 0)` raises.

```bash
python3.12 show_intervaltree.py
```

Pinned output: `results/SHOW_INTERVALTREE.json`.
