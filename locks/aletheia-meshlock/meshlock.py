#!/usr/bin/env python3.12
"""Meshlock — Delaunay triangle-count check."""

from __future__ import annotations

import argparse
import sys

from delaun import delaun_tris


def verify_precision() -> str:
    if delaun_tris([(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]) != 4:
        raise SystemExit("delaunay identity failed")
    if delaun_tris([(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]) != delaun_tris(
        [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]
    ):
        raise SystemExit("delaunay mismatch")
    try:
        delaun_tris([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty delaunay accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Meshlock — Delaunay triangle-count check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
