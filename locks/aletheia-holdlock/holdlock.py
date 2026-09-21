#!/usr/bin/env python3.12
"""Holdlock — couple-swap occupancy check."""
from __future__ import annotations
import argparse, sys
from couple import min_swaps_couples

def verify_precision() -> str:
    if min_swaps_couples([0,2,1,3])!=1:
        raise SystemExit("hold identity failed")
    if min_swaps_couples([3,2,0,1])!=0:
        raise SystemExit("already-paired identity failed")
    try:
        min_swaps_couples(None)
    except ValueError:
        pass
    else:
        raise SystemExit("missing row accepted")
    return "ok"

def main() -> int:
    p=argparse.ArgumentParser(description="Holdlock — couple-swap occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
