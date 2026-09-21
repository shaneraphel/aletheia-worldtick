#!/usr/bin/env python3.12
"""Kalmanlock — observation occupancy check."""
from __future__ import annotations
import argparse, sys
from kalman import kalman_filter

def verify_precision() -> str:
    if kalman_filter([(2, 0), (3, 1), (1, 0)]) != 3:
        raise SystemExit("kalman identity failed")
    if kalman_filter([(2, 0), (3, 1), (1, 0)]) != kalman_filter([(2, 0), (3, 1), (1, 0)]):
        raise SystemExit("kalman mismatch")
    try:
        kalman_filter([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty kalman accepted")
    return "ok"

def main() -> int:
    p = argparse.ArgumentParser(description="Kalmanlock — observation occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args = p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    p.print_help()
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
