#!/usr/bin/env python3.12
"""Use a stdlib dict as the hash table. Record empty get. Refuse empty keys."""
from __future__ import annotations
import json, platform, sys
from cuckoo import cuckoo_placed

def theirs() -> dict:
    empty = {}.get(3)
    placed = {3: True, 8: True, 12: True}
    return {"package": "stdlib-dict", "empty_get": empty, "n_keys": len(placed)}

def ours() -> dict:
    n = cuckoo_placed([3, 8, 12], 5)
    empty = "raised"
    try:
        cuckoo_placed([], 5)
        empty = "accepted"
    except ValueError:
        pass
    return {"cuckoo_placed": n, "empty": empty}

def main() -> int:
    rec = {"schema":"cuckoolock.show_dict.v1","used":"https://docs.python.org/3/library/stdtypes.html#dict","built":"three keys placed 3; empty key tape is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["cuckoo_placed"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("cuckoolock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
