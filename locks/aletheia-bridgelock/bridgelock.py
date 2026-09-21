#!/usr/bin/env python3.12
"""Bridgelock — Tarjan bridge occupancy check."""
from __future__ import annotations
import argparse, sys
from tarjan import n_bridges

def verify_precision() -> str:
    if n_bridges(4, [(0,1),(1,2),(2,0),(2,3)]) != 1:
        raise SystemExit("bridge identity failed")
    try:
        n_bridges(4, [])
    except ValueError:
        pass
    else:
        raise SystemExit("empty graph accepted")
    return "ok"

def main() -> int:
    p=argparse.ArgumentParser(description="Bridgelock — Tarjan bridge occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
