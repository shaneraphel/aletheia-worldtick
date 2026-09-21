#!/usr/bin/env python3.12
"""Clearlock — signed-distance occupancy check."""
from __future__ import annotations
import argparse, sys
from sdfocc import signed_distance_occupancy, disk_clearance2

def verify_precision() -> str:
    if signed_distance_occupancy([(3,0),(4,1),(2,0)]) != 3:
        raise SystemExit("sdf identity failed")
    if disk_clearance2(3,0,0,0,3) != 0:
        raise SystemExit("clearance identity failed")
    try:
        signed_distance_occupancy([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty sdf accepted")
    return "ok"

def main() -> int:
    p=argparse.ArgumentParser(description="Clearlock — signed-distance occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
