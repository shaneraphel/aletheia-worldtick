#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from visitall import shortest_path_visit
SEED, N_TRIALS, WARMUP = 20260919, 7, 1
G=[[1,2,3],[0],[0],[0]]
def main():
    a,b=[],[]; first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=shortest_path_visit(G); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=shortest_path_visit(G); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("tour disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first; second=acc
    if shortest_path_visit(G)!=4: raise SystemExit("identity")
    try: shortest_path_visit([])
    except ValueError: pass
    else: raise SystemExit("empty accepted")
    rec={"schema":"tourlock.visitall_bench.v1","seed":SEED,"n_nodes":4,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"tour_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"tour_seconds":a,"repeat_seconds":b,"len_first":first,"len_second":second,"len_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
