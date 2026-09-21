#!/usr/bin/env python3.12
"""Sicklock — infection-order occupancy check."""
from __future__ import annotations
import argparse, sys
from infsq import infection_sequences
def verify_precision() -> str:
    if infection_sequences(5, [0,4])!=4: raise SystemExit("sick identity failed")
    if infection_sequences(5, [0,4])!=infection_sequences(5, [0,4]): raise SystemExit("sick mismatch")
    try: infection_sequences(5, [])
    except ValueError: pass
    else: raise SystemExit("empty sick set accepted")
    return "ok"
def main() -> int:
    p=argparse.ArgumentParser(description="Sicklock — infection-order occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
