#!/usr/bin/env python3.12
"""Use munkres on a contact square. Record empty occupancy. Refuse here."""

from __future__ import annotations

import json
import platform
import sys

from hungar import hungar_cost


def theirs() -> dict:
    import munkres

    m = munkres.Munkres()
    cases: dict[str, object] = {}
    for key, mat in (("empty", []), ("nested_empty", [[]]), ("square", [[1, 2], [2, 1]])):
        try:
            cases[key] = m.compute(mat)
        except Exception as exc:
            cases[key] = f"{type(exc).__name__}: {exc}"
    return {"package": "munkres", "version": getattr(munkres, "__version__", "?"), "cases": cases}


def ours() -> dict:
    cost = hungar_cost([[1, 2], [2, 1]])
    empty = "raised"
    try:
        hungar_cost([])
        empty = "accepted"
    except ValueError:
        pass
    return {"hungar_cost_square": cost, "empty": empty}


def main() -> int:
    rec = {
        "schema": "handlock.show_munkres.v1",
        "used": "https://github.com/bmc/munkres",
        "note": "https://github.com/bmc/munkres/issues/54",
        "built": "2x2 finger-to-contact assignment; empty cost is absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["hungar_cost_square"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("handlock show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
