#!/usr/bin/env python3.12
"""Use bitarray rank on a spike tape. Record empty symbols. Refuse here."""

from __future__ import annotations

import json
import platform
import sys

from wavelet import wavelet_rank

SEQ = [1, 2, 1, 3, 1]


def theirs() -> dict:
    from bitarray import bitarray

    empty = bitarray()
    filled = bitarray(x == 1 for x in SEQ)
    return {
        "package": "bitarray",
        "version": __import__("importlib.metadata", fromlist=["version"]).version("bitarray"),
        "empty_count_1": int(empty.count(1)),
        "rank_1_through_5": int(filled.count(1)),
    }


def ours() -> dict:
    rank = wavelet_rank(SEQ, 1, 5)
    empty = "raised"
    try:
        wavelet_rank([], 1, 0)
        empty = "accepted"
    except ValueError:
        pass
    return {"wavelet_rank_1": rank, "empty": empty}


def main() -> int:
    rec = {
        "schema": "ranklock.show_bitarray.v1",
        "used": "https://github.com/ilanschnell/bitarray",
        "built": "five-symbol spike rank 3 of symbol 1; empty tape is absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["wavelet_rank_1"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("ranklock show identity failed")
    if rec["theirs"]["rank_1_through_5"] != 3:
        raise SystemExit("bitarray rank identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
