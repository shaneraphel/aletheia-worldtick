# Show: NetworkX (the empty residual)

Compared with [networkx/networkx](https://github.com/networkx/networkx) on a
four-node traffic diamond: the same max-flow 2, plus a refusal when the
residual tape is empty.

NetworkX 3.6.1 `maximum_flow_value` on four terminals and no edges is 0.
`dinic_max_flow(4, [], 0, 3)` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
