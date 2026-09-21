#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from racecr import race_car
SEED, T, N_TRIALS, WARMUP = 20260919, 6, 7, 1
def main():
    a,b=[],[]; first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=race_car(T); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=race_car(T); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("race disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first; second=acc
    if race_car(3)!=2: raise SystemExit("identity")
    try: race_car(-1)
    except ValueError: pass
    else: raise SystemExit("neg accepted")
    rec={"schema":"racelock.racecr_bench.v1","seed":SEED,"target":T,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"race_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"race_seconds":a,"repeat_seconds":b,"inst_first":first,"inst_second":second,"inst_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
