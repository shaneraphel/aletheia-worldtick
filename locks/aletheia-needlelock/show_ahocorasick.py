#!/usr/bin/env python3.12
"""Use pyahocorasick on a token tape. Record empty needle. Refuse here."""

from __future__ import annotations

import json
import platform
import sys

from acauto import aho_hits


def theirs() -> dict:
    import ahocorasick

    machine = ahocorasick.Automaton()
    try:
        machine.add_word("", 0)
        empty_add = "accepted"
    except Exception as exc:
        empty_add = f"{type(exc).__name__}: {exc}"
    machine.add_word("ab", 1)
    machine.add_word("bc", 2)
    machine.make_automaton()
    hits = list(machine.iter("abcabc"))
    return {
        "package": "pyahocorasick",
        "version": __import__("importlib.metadata", fromlist=["version"]).version("pyahocorasick"),
        "empty_add_word": empty_add,
        "hits_abcabc": len(hits),
    }


def ours() -> dict:
    hits = aho_hits("abcabc", ["ab", "bc"])
    empty = "raised"
    try:
        aho_hits("", ["ab"])
        empty = "accepted"
    except ValueError:
        pass
    return {"aho_hits_abcabc": hits, "empty": empty}


def main() -> int:
    rec = {
        "schema": "needlelock.show_ahocorasick.v1",
        "used": "https://github.com/WojciechMula/pyahocorasick",
        "note": "https://github.com/WojciechMula/pyahocorasick/issues/225",
        "built": "overlapping needle occupancy on abcabc; empty text is absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["aho_hits_abcabc"] != 4 or rec["ours"]["empty"] != "raised":
        raise SystemExit("needlelock show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
