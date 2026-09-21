#!/usr/bin/env python3.12
"""Obstlock — obstacle-elim occupancy check."""
from __future__ import annotations
import argparse, sys
from gridk import shortest_path_obstacles

GRID = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]]

def verify_precision() -> str:
    if shortest_path_obstacles(GRID, 1) != 6:
        raise SystemExit("obstacle identity failed")
    if shortest_path_obstacles(GRID, 1) != shortest_path_obstacles(GRID, 1):
        raise SystemExit("obstacle mismatch")
    try:
        shortest_path_obstacles([], 1)
    except ValueError:
        pass
    else:
        raise SystemExit("empty grid accepted")
    return "ok"

def main() -> int:
    p = argparse.ArgumentParser(description="Obstlock — obstacle-elim occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args = p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__ == "__main__":
    raise SystemExit(main())
