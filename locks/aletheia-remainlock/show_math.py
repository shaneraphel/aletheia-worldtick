#!/usr/bin/env python3.12
"""Use math.gcd on a clock remainder. Record missing modulus. Refuse here."""
from __future__ import annotations
import json, math, platform, sys
from crt import crt_pair

def theirs() -> dict:
    return {"package":"math","empty_gcd":math.gcd(0,0),"gcd_3_5":math.gcd(3,5)}

def ours() -> dict:
    v = crt_pair(2,3,3,5)
    empty = "raised"
    try:
        crt_pair(2,0,3,5)
        empty = "accepted"
    except ValueError:
        pass
    return {"crt_pair": v, "empty": empty}

def main() -> int:
    rec = {"schema":"remainlock.show_math.v1","used":"https://docs.python.org/3/library/math.html","built":"two-modulus clock remainder 8; missing modulus is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["crt_pair"] != 8 or rec["ours"]["empty"] != "raised":
        raise SystemExit("remainlock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
