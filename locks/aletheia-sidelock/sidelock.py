#!/usr/bin/env python3.12
"""Sidelock — left-visible occupancy check."""
from __future__ import annotations
import argparse, sys
from visst import ways_rearrange_sticks

def verify_precision() -> str:
    if ways_rearrange_sticks(3, 2) != 3:
        raise SystemExit("side identity failed")
    if ways_rearrange_sticks(3, 2) != ways_rearrange_sticks(3, 2):
        raise SystemExit("side mismatch")
    try:
        ways_rearrange_sticks(0, 1)
    except ValueError:
        pass
    else:
        raise SystemExit("empty n accepted")
    return "ok"

def main() -> int:
    p=argparse.ArgumentParser(description="Sidelock — left-visible occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
