#!/usr/bin/env python3.12
"""Stemlock — Ukkonen suffix-link occupancy check."""

from __future__ import annotations

import argparse
import sys

from ukkonen import n_suffix_links


def verify_precision() -> str:
    if n_suffix_links("aba") != 3:
        raise SystemExit("ukkonen identity failed")
    if n_suffix_links("aba") != n_suffix_links("aba"):
        raise SystemExit("ukkonen mismatch")
    try:
        n_suffix_links("")
    except ValueError:
        pass
    else:
        raise SystemExit("empty ukkonen accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Stemlock — Ukkonen suffix-link occupancy check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
