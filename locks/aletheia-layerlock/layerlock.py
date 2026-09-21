#!/usr/bin/env python3.12
"""Layerlock — Kahn layer occupancy check."""

from __future__ import annotations

import argparse
import sys

from kahn import kahn_layers


def verify_precision() -> str:
    if kahn_layers(3, [(0, 1), (1, 2)]) != 3:
        raise SystemExit("kahn identity failed")
    if kahn_layers(3, [(0, 1), (1, 2)]) != kahn_layers(3, [(0, 1), (1, 2)]):
        raise SystemExit("kahn mismatch")
    try:
        kahn_layers(-1, [])
    except ValueError:
        pass
    else:
        raise SystemExit("negative kahn accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Layerlock — Kahn layer occupancy check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
