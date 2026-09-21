#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from coinp import cheapest_jump
SEED, N_TRIALS, WARMUP = 20260919, 7, 1
COINS=[1,2,4,-1,2]
def main():
    a,b=[],[]; first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=cheapest_jump(COINS,2); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=cheapest_jump(COINS,2); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("coin disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first; second=acc
    if cheapest_jump(COINS,2)!=[1,3,5]: raise SystemExit("identity")
    try: cheapest_jump([],2)
    except ValueError: pass
    else: raise SystemExit("empty accepted")
    rec={"schema":"coinlock.coinp_bench.v1","seed":SEED,"n_coins":len(COINS),"max_jump":2,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"coin_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"coin_seconds":a,"repeat_seconds":b,"path_first":first,"path_second":second,"path_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
