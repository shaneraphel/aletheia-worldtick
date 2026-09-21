#!/usr/bin/env python3.12
"""Climblock — longest-increasing-path occupancy check."""
from __future__ import annotations
import argparse, sys
from lipath import longest_increasing_path

M = [[9,9,4],[6,6,8],[2,1,1]]

def verify_precision() -> str:
    if longest_increasing_path(M) != 4:
        raise SystemExit("climb identity failed")
    if longest_increasing_path(M) != longest_increasing_path(M):
        raise SystemExit("climb mismatch")
    try:
        longest_increasing_path([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty matrix accepted")
    return "ok"

def main() -> int:
    p=argparse.ArgumentParser(description="Climblock — longest-increasing-path occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
