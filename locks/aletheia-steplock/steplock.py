#!/usr/bin/env python3.12
"""Steplock — Runge–Kutta tableau occupancy check."""

from __future__ import annotations

import argparse
import sys

from rkutta import runge_kutta


def verify_precision() -> str:
    if runge_kutta([(1, 0), (2, 1)]) != 2:
        raise SystemExit("rk identity failed")
    if runge_kutta([(1, 0), (2, 1)]) != runge_kutta([(1, 0), (2, 1)]):
        raise SystemExit("rk mismatch")
    try:
        runge_kutta([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty runge-kutta accepted")
    try:
        runge_kutta([(0, 1)])
    except ValueError:
        pass
    else:
        raise SystemExit("non-positive stages accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Steplock — Runge–Kutta tableau occupancy check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
