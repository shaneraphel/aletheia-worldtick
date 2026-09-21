#!/usr/bin/env python3.12
"""Use NumPy prefix compare on banana. Record empty text. Refuse here."""
from __future__ import annotations
import json, platform, sys
from kasai import kasai_lcp_at

def theirs() -> dict:
    import numpy as np
    a = np.frombuffer(b"", dtype=np.uint8)
    empty = int(np.sum(a == a))
    x = np.frombuffer(b"ana", dtype=np.uint8)
    y = np.frombuffer(b"anana", dtype=np.uint8)
    n = int(np.sum(np.cumprod(x[:len(y)] == y[:len(x)])))
    return {"package":"numpy","version":np.__version__,"empty_common":empty,"ana_anana":n}

def ours() -> dict:
    n = kasai_lcp_at("banana", [5,3,1,0,4,2], 2)
    empty = "raised"
    try:
        kasai_lcp_at("", [], 0)
        empty = "accepted"
    except ValueError:
        pass
    return {"kasai_lcp_at": n, "empty": empty}

def main() -> int:
    rec = {"schema":"lcplock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"banana LCP 3 at index 2; empty suffix tape is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["kasai_lcp_at"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("lcplock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
