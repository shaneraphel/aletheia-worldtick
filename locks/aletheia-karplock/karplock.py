#!/usr/bin/env python3.12
"""Karplock — Hopcroft–Karp matching check."""

from __future__ import annotations

import argparse
import sys

from hopcroft import hopcroft_karp


def verify_precision() -> str:
    if hopcroft_karp(2, 2, [(0, 0), (0, 1), (1, 1)]) != 2:
        raise SystemExit("hopcroft identity failed")
    if hopcroft_karp(2, 2, [(0, 0), (0, 1), (1, 1)]) != hopcroft_karp(
        2, 2, [(0, 0), (0, 1), (1, 1)]
    ):
        raise SystemExit("hopcroft mismatch")
    try:
        hopcroft_karp(2, 2, [])
    except ValueError:
        pass
    else:
        raise SystemExit("empty hopcroft accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Karplock — Hopcroft–Karp matching check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
