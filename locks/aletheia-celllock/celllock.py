#!/usr/bin/env python3.12
"""Celllock — Voronoi unbounded-cell check."""

from __future__ import annotations

import argparse
import sys

from voronoi import voronoi_unbounded


def verify_precision() -> str:
    if voronoi_unbounded([(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]) != 4:
        raise SystemExit("voronoi identity failed")
    if voronoi_unbounded([(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]) != voronoi_unbounded(
        [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]
    ):
        raise SystemExit("voronoi mismatch")
    try:
        voronoi_unbounded([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty voronoi accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Celllock — Voronoi unbounded-cell check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
