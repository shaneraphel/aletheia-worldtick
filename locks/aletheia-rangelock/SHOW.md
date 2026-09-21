# Show: I used sortedcontainers, and I refused the empty point tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [grantjenks/python-sortedcontainers](https://github.com/grantjenks/python-sortedcontainers)
on three lane contacts: the same box count 2, plus a refusal when the point
tape is empty.

sortedcontainers 2.4.0 `irange` on an empty SortedList is `[]`.
`rngtree_count([], 0, 2, 0, 2)` raises.

```bash
python3.12 show_sortedcontainers.py
```

Pinned output: `results/SHOW_SORTEDCONTAINERS.json`.
