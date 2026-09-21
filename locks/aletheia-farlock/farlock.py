#!/usr/bin/env python3.12
"""Farlock — Manhattan-span occupancy check."""
from __future__ import annotations
import argparse, sys
from manh import min_manhattan_after_remove
PTS=[[3,10],[5,15],[10,2],[4,4]]
def verify_precision() -> str:
    if min_manhattan_after_remove(PTS)!=12: raise SystemExit("far identity failed")
    if min_manhattan_after_remove(PTS)!=min_manhattan_after_remove(PTS): raise SystemExit("far mismatch")
    try: min_manhattan_after_remove([])
    except ValueError: pass
    else: raise SystemExit("empty points accepted")
    return "ok"
def main() -> int:
    p=argparse.ArgumentParser(description="Farlock — Manhattan-span occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
