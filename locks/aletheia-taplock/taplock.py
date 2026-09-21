#!/usr/bin/env python3.12
"""Taplock — garden-tap occupancy check."""
from __future__ import annotations
import argparse, sys
from tapsg import min_taps
R=[3,4,1,1,0,0]
def verify_precision() -> str:
    if min_taps(5, R)!=1: raise SystemExit("tap identity failed")
    if min_taps(5, R)!=min_taps(5, R): raise SystemExit("tap mismatch")
    try: min_taps(0, [])
    except ValueError: pass
    else: raise SystemExit("empty n accepted")
    return "ok"
def main() -> int:
    p=argparse.ArgumentParser(description="Taplock — garden-tap occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
