# Show: kdtree (the empty contact tape)

Compared with [stefankoegl/kdtree](https://github.com/stefankoegl/kdtree) on a
contact tape: nearest-x for `(3, 4)` among `[(0,0),(3,4)]`, plus a refusal
when there are no points.

`create(dimensions=2).search_nn((0,0))` returns `None` there. `kdtree_near([])`
raises. The note on their tree is
[stefankoegl/kdtree#56](https://github.com/stefankoegl/kdtree/issues/56).

```bash
python3.12 show_kdtree.py
```

Pinned output: `results/SHOW_KDTREE.json`.
