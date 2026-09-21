#!/usr/bin/env python3.12
"""Hookelock — spring occupancy check."""
from __future__ import annotations
import argparse, sys
from hooke import hooke_law

def verify_precision() -> str:
    if hooke_law([(3, 0), (4, 1), (2, 0)]) != 3:
        raise SystemExit("hooke identity failed")
    if hooke_law([(3, 0), (4, 1), (2, 0)]) != hooke_law([(3, 0), (4, 1), (2, 0)]):
        raise SystemExit("hooke mismatch")
    try:
        hooke_law([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty hooke accepted")
    return "ok"

def main() -> int:
    p = argparse.ArgumentParser(description="Hookelock — spring occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args = p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    p.print_help()
    return 2
if __name__ == "__main__":
    raise SystemExit(main())
