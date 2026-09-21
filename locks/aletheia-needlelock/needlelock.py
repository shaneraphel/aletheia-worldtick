#!/usr/bin/env python3.12
"""Needlelock — Aho–Corasick hit-count check."""

from __future__ import annotations

import argparse
import sys

from acauto import aho_hits


def verify_precision() -> str:
    if aho_hits("abcabc", ["ab", "bc"]) != 4:
        raise SystemExit("aho identity failed")
    if aho_hits("abcabc", ["ab", "bc"]) != aho_hits("abcabc", ["ab", "bc"]):
        raise SystemExit("aho mismatch")
    try:
        aho_hits("", ["ab"])
    except ValueError:
        pass
    else:
        raise SystemExit("empty text accepted")
    try:
        aho_hits("abc", [""])
    except ValueError:
        pass
    else:
        raise SystemExit("empty pattern accepted")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Needlelock precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
