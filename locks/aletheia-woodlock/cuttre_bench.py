#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from cuttre import cut_off_trees
SEED, N_TRIALS, WARMUP = 20260919, 7, 1
F=[[1,2,3],[0,0,4],[7,6,5]]
def main():
    a,b=[],[]; first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=cut_off_trees(F); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=cut_off_trees(F); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("wood disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first; second=acc
    if cut_off_trees(F)!=6: raise SystemExit("identity")
    try: cut_off_trees([])
    except ValueError: pass
    else: raise SystemExit("empty accepted")
    rec={"schema":"woodlock.cuttre_bench.v1","seed":SEED,"n_rows":3,"n_cols":3,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"cut_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"cut_seconds":a,"repeat_seconds":b,"steps_first":first,"steps_second":second,"steps_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
