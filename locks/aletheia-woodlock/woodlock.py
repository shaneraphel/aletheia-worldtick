#!/usr/bin/env python3.12
"""Woodlock — forest-cut occupancy check."""
from __future__ import annotations
import argparse, sys
from cuttre import cut_off_trees
F=[[1,2,3],[0,0,4],[7,6,5]]
def verify_precision() -> str:
    if cut_off_trees(F)!=6: raise SystemExit("wood identity failed")
    if cut_off_trees(F)!=cut_off_trees(F): raise SystemExit("wood mismatch")
    try: cut_off_trees([])
    except ValueError: pass
    else: raise SystemExit("empty forest accepted")
    return "ok"
def main() -> int:
    p=argparse.ArgumentParser(description="Woodlock — forest-cut occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
