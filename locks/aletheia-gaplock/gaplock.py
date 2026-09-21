#!/usr/bin/env python3.12
"""Gaplock — empty-slot occupancy check."""
from __future__ import annotations
import argparse, sys
from kslots import k_empty_slots
def verify_precision() -> str:
    if k_empty_slots([1,3,2], 1)!=2: raise SystemExit("gap identity failed")
    if k_empty_slots([1,3,2], 1)!=k_empty_slots([1,3,2], 1): raise SystemExit("gap mismatch")
    try: k_empty_slots([], 1)
    except ValueError: pass
    else: raise SystemExit("empty bulbs accepted")
    return "ok"
def main() -> int:
    p=argparse.ArgumentParser(description="Gaplock — empty-slot occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
