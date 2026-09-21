#!/usr/bin/env python3.12
"""Jumplock — frog-jump occupancy check."""
from __future__ import annotations
import argparse, sys
from frogjp import can_cross
STONES=[0,1,3,5,6,8,12,17]
def verify_precision() -> str:
    if can_cross(STONES) is not True: raise SystemExit("jump identity failed")
    if can_cross(STONES)!=can_cross(STONES): raise SystemExit("jump mismatch")
    try: can_cross([])
    except ValueError: pass
    else: raise SystemExit("empty stones accepted")
    return "ok"
def main() -> int:
    p=argparse.ArgumentParser(description="Jumplock — frog-jump occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
