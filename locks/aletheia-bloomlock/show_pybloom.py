#!/usr/bin/env python3.12
"""Use pybloom-live on a spike filter. Record empty keys. Refuse here."""

from __future__ import annotations

import json
import platform
import sys

from bloom import bloom_maybe


def theirs() -> dict:
    from importlib.metadata import version
    from pybloom_live import BloomFilter

    empty = BloomFilter(capacity=10, error_rate=0.1)
    filled = BloomFilter(capacity=10, error_rate=0.1)
    for x in (1, 2, 3):
        filled.add(x)
    return {
        "package": "pybloom-live",
        "version": version("pybloom_live"),
        "empty_membership_2": bool(2 in empty),
        "filled_membership_2": bool(2 in filled),
    }


def ours() -> dict:
    maybe = bloom_maybe([1, 2, 3], 16, 2, 2)
    empty = "raised"
    try:
        bloom_maybe([], 16, 2, 2)
        empty = "accepted"
    except ValueError:
        pass
    return {"bloom_maybe_2": maybe, "empty": empty}


def main() -> int:
    rec = {
        "schema": "bloomlock.show_pybloom.v1",
        "used": "https://github.com/joseph-fox/python-bloomfilter",
        "built": "three-key spike maybe-membership 1; empty keys are absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["bloom_maybe_2"] != 1 or rec["ours"]["empty"] != "raised":
        raise SystemExit("bloomlock show identity failed")
    if rec["theirs"]["filled_membership_2"] is not True:
        raise SystemExit("pybloom filled identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
