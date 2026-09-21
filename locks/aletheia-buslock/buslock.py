#!/usr/bin/env python3.12
"""Buslock — bus-route occupancy check."""
from __future__ import annotations
import argparse, sys
from busrts import num_buses

R=[[1,2,7],[3,6,7]]

def verify_precision() -> str:
    if num_buses(R,1,6)!=2:
        raise SystemExit("bus identity failed")
    if num_buses(R,1,6)!=num_buses(R,1,6):
        raise SystemExit("bus mismatch")
    try:
        num_buses(None,1,6)
    except ValueError:
        pass
    else:
        raise SystemExit("missing routes accepted")
    return "ok"

def main() -> int:
    p=argparse.ArgumentParser(description="Buslock — bus-route occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
