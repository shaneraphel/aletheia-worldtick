#!/usr/bin/env python3.12
"""Flowlock — Dinic blocking-flow check."""

from __future__ import annotations

import argparse
import sys

from dinic import dinic_max_flow


def verify_precision() -> str:
    if dinic_max_flow(4, [(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1)], 0, 3) != 2:
        raise SystemExit("dinic identity failed")
    if dinic_max_flow(4, [(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1)], 0, 3) != dinic_max_flow(
        4, [(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1)], 0, 3
    ):
        raise SystemExit("dinic mismatch")
    try:
        dinic_max_flow(4, [], 0, 3)
    except ValueError:
        pass
    else:
        raise SystemExit("empty dinic accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Flowlock — Dinic blocking-flow check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
