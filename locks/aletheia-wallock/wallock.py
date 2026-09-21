#!/usr/bin/env python3.12
"""Wallock — min-obstacle-removal occupancy check."""
from __future__ import annotations
import argparse, sys
from obstc import min_obstacle_removal

GRID = [[0,1,1],[1,1,0],[1,1,0]]

def verify_precision() -> str:
    if min_obstacle_removal(GRID) != 2:
        raise SystemExit("wall identity failed")
    if min_obstacle_removal(GRID) != min_obstacle_removal(GRID):
        raise SystemExit("wall mismatch")
    try:
        min_obstacle_removal([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty grid accepted")
    return "ok"

def main() -> int:
    p=argparse.ArgumentParser(description="Wallock — min-obstacle-removal occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
