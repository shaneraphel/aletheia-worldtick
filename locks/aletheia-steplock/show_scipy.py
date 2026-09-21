#!/usr/bin/env python3.12
"""Use SciPy solve_ivp on an embodiment tape. Record empty tableau. Refuse here."""
from __future__ import annotations
import json, platform, sys
from rkutta import runge_kutta

def theirs() -> dict:
    from scipy.integrate import solve_ivp
    sol = solve_ivp(lambda t,y: -y, [0, 0], [1.0])
    return {"package":"scipy","version":__import__("scipy").__version__,"zero_span_t":int(sol.t.size)}

def ours() -> dict:
    n = runge_kutta([(1,0),(2,1)])
    empty = "raised"
    try:
        runge_kutta([])
        empty = "accepted"
    except ValueError:
        pass
    return {"runge_kutta": n, "empty": empty}

def main() -> int:
    rec = {"schema":"steplock.show_scipy.v1","used":"https://github.com/scipy/scipy","built":"two-row Butcher occupancy 2; empty tableau is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["runge_kutta"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("steplock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
