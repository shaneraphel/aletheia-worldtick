#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, sys
from cuttre import cut_off_trees
F=[[1,2,3],[0,0,4],[7,6,5]]
def theirs():
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_norm":float(np.linalg.norm(np.array([]))),"n_cells":9}
def ours():
    n=cut_off_trees(F); empty="raised"
    try:
        cut_off_trees([]); empty="accepted"
    except ValueError:
        pass
    return {"cut_off_trees": n, "empty": empty}
def main():
    rec={"schema":"woodlock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"3x3 forest steps 6; empty forest is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["cut_off_trees"]!=6 or rec["ours"]["empty"]!="raised":
        raise SystemExit("woodlock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
