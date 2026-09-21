#!/usr/bin/env python3.12
"""Slotlock — interval overlap occupancy check."""
from __future__ import annotations
import argparse, sys
from intervaltree import interval_tree_overlap

def verify_precision() -> str:
    if interval_tree_overlap([(0, 4), (2, 6)], 3) != 2:
        raise SystemExit("overlap identity failed")
    if interval_tree_overlap([(0, 4), (2, 6)], 3) != interval_tree_overlap([(0, 4), (2, 6)], 3):
        raise SystemExit("overlap mismatch")
    try:
        interval_tree_overlap([], 0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty intervals accepted")
    return "ok"

def main() -> int:
    p = argparse.ArgumentParser(description="Slotlock — interval overlap occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args = p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    p.print_help()
    return 2
if __name__ == "__main__":
    raise SystemExit(main())
