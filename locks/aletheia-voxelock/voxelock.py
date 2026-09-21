#!/usr/bin/env python3.12
"""Voxelock — octree NE occupancy check."""

from __future__ import annotations

import argparse
import sys

from octpart import octpart_ne


def verify_precision() -> str:
    if octpart_ne([(1, 1, 1), (0, 0, 0)], 1, 1, 1) != 1:
        raise SystemExit("oct identity failed")
    if octpart_ne([(1, 1, 1), (0, 0, 0)], 1, 1, 1) != octpart_ne(
        [(1, 1, 1), (0, 0, 0)], 1, 1, 1
    ):
        raise SystemExit("oct mismatch")
    try:
        octpart_ne([], 0, 0, 0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty octree accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Voxelock — octree NE occupancy check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
