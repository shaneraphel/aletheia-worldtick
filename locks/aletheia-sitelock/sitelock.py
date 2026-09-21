#!/usr/bin/env python3.12
"""Sitelock — Fortune Voronoi-vertex check."""

from __future__ import annotations

import argparse
import sys

from fortun import fortun_verts


def verify_precision() -> str:
    if fortun_verts([(0, 0), (2, 0), (1, 2)]) != 1:
        raise SystemExit("fortune identity failed")
    if fortun_verts([(0, 0), (2, 0), (1, 2)]) != fortun_verts([(0, 0), (2, 0), (1, 2)]):
        raise SystemExit("fortune mismatch")
    try:
        fortun_verts([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty fortune accepted")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Sitelock precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
