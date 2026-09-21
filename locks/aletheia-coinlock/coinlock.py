#!/usr/bin/env python3.12
"""Coinlock — cheapest coin-path occupancy check."""
from __future__ import annotations
import argparse, sys
from coinp import cheapest_jump
COINS=[1,2,4,-1,2]
def verify_precision() -> str:
    if cheapest_jump(COINS, 2)!=[1,3,5]: raise SystemExit("coin identity failed")
    if cheapest_jump(COINS, 2)!=cheapest_jump(COINS, 2): raise SystemExit("coin mismatch")
    try: cheapest_jump([], 2)
    except ValueError: pass
    else: raise SystemExit("empty coins accepted")
    return "ok"
def main() -> int:
    p=argparse.ArgumentParser(description="Coinlock — cheapest coin-path occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
