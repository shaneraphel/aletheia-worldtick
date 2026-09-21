#!/usr/bin/env python3.12
"""Fingerlock — two-finger occupancy check."""
from __future__ import annotations
import argparse, sys
from twofng import minimum_distance

def verify_precision() -> str:
    if minimum_distance("CAKE") != 3:
        raise SystemExit("finger identity failed")
    if minimum_distance("CAKE") != minimum_distance("CAKE"):
        raise SystemExit("finger mismatch")
    try:
        minimum_distance("")
    except ValueError:
        pass
    else:
        raise SystemExit("empty word accepted")
    return "ok"

def main() -> int:
    p = argparse.ArgumentParser(description="Fingerlock — two-finger occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args = p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__ == "__main__":
    raise SystemExit(main())
