#!/usr/bin/env python3.12
"""Rangelock — range-tree box occupancy check."""

from __future__ import annotations

import argparse
import sys

from rngtree import rngtree_count


def verify_precision() -> str:
    if rngtree_count([(0, 0), (1, 1), (3, 3)], 0, 2, 0, 2) != 2:
        raise SystemExit("range identity failed")
    if rngtree_count([(0, 0), (1, 1), (3, 3)], 0, 2, 0, 2) != rngtree_count(
        [(0, 0), (1, 1), (3, 3)], 0, 2, 0, 2
    ):
        raise SystemExit("range mismatch")
    try:
        rngtree_count([], 0, 1, 0, 1)
    except ValueError:
        pass
    else:
        raise SystemExit("empty range tree accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Rangelock — range-tree box occupancy check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
