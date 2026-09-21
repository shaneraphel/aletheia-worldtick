#!/usr/bin/env python3.12
"""Routelock — Johnson routing-distance check."""

from __future__ import annotations

import argparse
import sys

from johnson import johnson_dist


def verify_precision() -> str:
    if johnson_dist(3, [(0, 1, 1), (1, 2, 1)], 0, 2) != 2:
        raise SystemExit("johnson identity failed")
    if johnson_dist(3, [(0, 1, 1), (1, 2, 1)], 0, 2) != johnson_dist(
        3, [(0, 1, 1), (1, 2, 1)], 0, 2
    ):
        raise SystemExit("johnson mismatch")
    try:
        johnson_dist(3, [], 0, 2)
    except ValueError:
        pass
    else:
        raise SystemExit("empty edges accepted")
    try:
        johnson_dist(2, [(0, 1, -1), (1, 0, -1)], 0, 1)
    except ValueError:
        pass
    else:
        raise SystemExit("negative cycle accepted")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Routelock precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
