#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from jobsc import job_scheduling
SEED, N_TRIALS, WARMUP = 20260919, 7, 1
S,E,P=[1,2,3,3],[3,4,5,6],[50,10,40,70]
def main():
    a,b=[],[]; first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=job_scheduling(S,E,P); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=job_scheduling(S,E,P); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("shift disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first; second=acc
    if job_scheduling(S,E,P)!=120: raise SystemExit("identity")
    try: job_scheduling([],[],[])
    except ValueError: pass
    else: raise SystemExit("empty accepted")
    rec={"schema":"shiftlock.jobsc_bench.v1","seed":SEED,"n_jobs":4,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"job_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"job_seconds":a,"repeat_seconds":b,"profit_first":first,"profit_second":second,"profit_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
