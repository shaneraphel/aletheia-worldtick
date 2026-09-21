#!/usr/bin/env python3.12
"""Gridlock — quadtree NE occupancy check."""

from __future__ import annotations

import argparse
import sys

from qdtree import qdtree_ne


def verify_precision() -> str:
    if qdtree_ne([(1, 1), (0, 0)], 1, 1) != 1:
        raise SystemExit("quad identity failed")
    if qdtree_ne([(1, 1), (0, 0)], 1, 1) != qdtree_ne([(1, 1), (0, 0)], 1, 1):
        raise SystemExit("quad mismatch")
    try:
        qdtree_ne([], 0, 0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty quadtree accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Gridlock — quadtree NE occupancy check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
