#!/usr/bin/env python3.12
"""Ticklock — Verlet step-occupancy check."""

from __future__ import annotations

import argparse
import sys

from verlet import verlet_integration


def verify_precision() -> str:
    if verlet_integration([(1, 0), (2, 1)]) != 2:
        raise SystemExit("verlet identity failed")
    if verlet_integration([(1, 0), (2, 1)]) != verlet_integration([(1, 0), (2, 1)]):
        raise SystemExit("verlet mismatch")
    try:
        verlet_integration([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty steps accepted")
    try:
        verlet_integration([(0, 1)])
    except ValueError:
        pass
    else:
        raise SystemExit("non-positive steps accepted")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Ticklock precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
