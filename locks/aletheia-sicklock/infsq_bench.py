#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from infsq import infection_sequences
SEED, N_TRIALS, WARMUP = 20260919, 7, 1
def main():
    a,b=[],[]; first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=infection_sequences(5,[0,4]); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=infection_sequences(5,[0,4]); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("sick disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first; second=acc
    if infection_sequences(5,[0,4])!=4: raise SystemExit("identity")
    try: infection_sequences(5,[])
    except ValueError: pass
    else: raise SystemExit("empty accepted")
    rec={"schema":"sicklock.infsq_bench.v1","seed":SEED,"n":5,"sick":[0,4],"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"sick_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"sick_seconds":a,"repeat_seconds":b,"seq_first":first,"seq_second":second,"seq_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
