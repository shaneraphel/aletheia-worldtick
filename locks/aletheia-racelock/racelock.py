#!/usr/bin/env python3.12
"""Racelock — instruction occupancy check."""
from __future__ import annotations
import argparse, sys
from racecr import race_car
def verify_precision() -> str:
    if race_car(3)!=2: raise SystemExit("race identity failed")
    if race_car(3)!=race_car(3): raise SystemExit("race mismatch")
    try: race_car(-1)
    except ValueError: pass
    else: raise SystemExit("negative target accepted")
    return "ok"
def main() -> int:
    p=argparse.ArgumentParser(description="Racelock — instruction occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
