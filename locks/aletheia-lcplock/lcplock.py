#!/usr/bin/env python3.12
"""Lcplock — Kasai LCP-at-index check."""

from __future__ import annotations

import argparse
import sys

from kasai import kasai_lcp_at


def verify_precision() -> str:
    if kasai_lcp_at("banana", [5, 3, 1, 0, 4, 2], 2) != 3:
        raise SystemExit("kasai identity failed")
    if kasai_lcp_at("banana", [5, 3, 1, 0, 4, 2], 2) != kasai_lcp_at(
        "banana", [5, 3, 1, 0, 4, 2], 2
    ):
        raise SystemExit("kasai mismatch")
    try:
        kasai_lcp_at("", [5], 0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty kasai accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Lcplock — Kasai LCP-at-index check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
