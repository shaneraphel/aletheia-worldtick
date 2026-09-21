#!/usr/bin/env python3.12
"""Camlock — camera-cover occupancy check."""
from __future__ import annotations
import argparse, sys
from camtree import min_camera_cover

def verify_precision() -> str:
    if min_camera_cover([0]) != 1:
        raise SystemExit("camera identity failed")
    if min_camera_cover([0]) != min_camera_cover([0]):
        raise SystemExit("camera mismatch")
    try:
        min_camera_cover(None)
    except ValueError:
        pass
    else:
        raise SystemExit("empty tree accepted")
    return "ok"

def main() -> int:
    p = argparse.ArgumentParser(description="Camlock — camera-cover occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args = p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__ == "__main__":
    raise SystemExit(main())
