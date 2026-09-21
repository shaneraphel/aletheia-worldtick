#!/usr/bin/env python3.12
"""Treaplock — treap-root occupancy check."""

from __future__ import annotations

import argparse
import sys

from treap import treap_root


def verify_precision() -> str:
    if treap_root([5, 3, 8], [2, 4, 1]) != 3:
        raise SystemExit("treap identity failed")
    if treap_root([5, 3, 8], [2, 4, 1]) != treap_root([5, 3, 8], [2, 4, 1]):
        raise SystemExit("treap mismatch")
    try:
        treap_root([], [])
    except ValueError:
        pass
    else:
        raise SystemExit("empty treap accepted")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Treaplock — treap-root occupancy check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
