#!/usr/bin/env python3.12
"""Nearlock — kd-tree nearest-x check."""

from __future__ import annotations

import argparse
import sys

from kdtree import kdtree_near


def verify_precision() -> str:
    if kdtree_near([(0, 0), (3, 4)], 3, 4) != 3:
        raise SystemExit("kd identity failed")
    if kdtree_near([(0, 0), (3, 4)], 3, 4) != kdtree_near([(0, 0), (3, 4)], 3, 4):
        raise SystemExit("kd mismatch")
    try:
        kdtree_near([], 0, 0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty kd-tree accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Nearlock — kd-tree nearest-x check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
