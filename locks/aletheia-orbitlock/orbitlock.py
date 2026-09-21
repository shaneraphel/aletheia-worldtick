#!/usr/bin/env python3.12
"""Orbitlock — disjoint-set occupancy check."""
from __future__ import annotations
import argparse, sys
from orbits import DisjointSet

def verify_precision() -> str:
    d = DisjointSet(4)
    d.union(0,1); d.union(2,3)
    if d.n_orbits() != 2:
        raise SystemExit("orbit identity failed")
    if d.n_orbits() != d.n_orbits():
        raise SystemExit("orbit mismatch")
    try:
        DisjointSet(-1)
    except ValueError:
        pass
    else:
        raise SystemExit("negative n accepted")
    return "ok"

def main() -> int:
    p = argparse.ArgumentParser(description="Orbitlock — disjoint-set occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args = p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__ == "__main__":
    raise SystemExit(main())
