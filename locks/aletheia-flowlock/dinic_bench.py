#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from collections import deque
from dinic import dinic_max_flow
SEED, N, N_TRIALS, WARMUP = 20260919, 24, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if rng.randrange(0, 3) == 0:
                edges.append((u, v, rng.randrange(1, 5)))
    if not edges:
        edges.append((0, n - 1, 1))
    return edges

def ford(n, edges, s, t):
    g = [[] for _ in range(n)]
    caps = []
    def add(u, v, c):
        g[u].append((v, len(caps))); caps.append(c)
        g[v].append((u, len(caps))); caps.append(0)
    for u, v, c in edges:
        add(u, v, c)
    flow = 0
    while True:
        parent = [-1] * n
        q = deque([s]); parent[s] = s
        found = False
        while q:
            u = q.popleft()
            for v, i in g[u]:
                if caps[i] > 0 and parent[v] < 0:
                    parent[v] = u
                    q.append(v)
                    if v == t:
                        found = True
                        break
            if found:
                break
        if not found:
            return flow
        path = []
        v = t
        while v != s:
            u = parent[v]
            for w, i in g[u]:
                if w == v and caps[i] > 0:
                    path.append(i); v = u; break
        addf = min(caps[i] for i in path)
        for i in path:
            caps[i] -= addf; caps[i ^ 1] += addf
        flow += addf

def main():
    edges = tape(N, SEED)
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = dinic_max_flow(N, edges, 0, N-1); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = ford(N, edges, 0, N-1); bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("dinic and ford disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if dinic_max_flow(4, [(0,1,1),(0,2,1),(1,3,1),(2,3,1)], 0, 3) != 2:
        raise SystemExit("identity")
    try:
        dinic_max_flow(4, [], 0, 3)
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "flowlock.dinic_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "dinic_seconds_median": statistics.median(a),
        "ford_seconds_median": statistics.median(b),
        "dinic_seconds": a, "ford_seconds": b,
        "flow_first": first, "flow_second": second,
        "flow_identical": first == second, "flow_equals_ford": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
