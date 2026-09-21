#!/usr/bin/env python3.12
"""Floodlock — rising-water occupancy check."""
from __future__ import annotations
import argparse, sys
from swimwt import swim_rising

G=[[0,2],[1,3]]

def verify_precision() -> str:
    if swim_rising(G)!=3:
        raise SystemExit("flood identity failed")
    if swim_rising(G)!=swim_rising(G):
        raise SystemExit("flood mismatch")
    try:
        swim_rising([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty grid accepted")
    return "ok"

def main() -> int:
    p=argparse.ArgumentParser(description="Floodlock — rising-water occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
