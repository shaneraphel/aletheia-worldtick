#!/usr/bin/env python3.12
"""Hulllock — Graham hull-occupancy check."""

from __future__ import annotations

import argparse
import sys

from graham import graham_hull


def verify_precision() -> str:
    if graham_hull([(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]) != 4:
        raise SystemExit("graham identity failed")
    if graham_hull([(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]) != graham_hull(
        [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]
    ):
        raise SystemExit("graham mismatch")
    try:
        graham_hull([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty points accepted")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Hulllock precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
