#!/usr/bin/env python3.12
"""Use pyahocorasick on aba. Record empty add_word. Refuse empty text."""
from __future__ import annotations
import json, platform, sys
from ukkonen import n_suffix_links

def theirs() -> dict:
    import ahocorasick
    A = ahocorasick.Automaton()
    empty = "accepted"
    try:
        A.add_word("", 0)
    except Exception:
        empty = "raised"
    A2 = ahocorasick.Automaton()
    A2.add_word("aba", 1)
    A2.make_automaton()
    return {"package":"pyahocorasick","version":"2.3.1","empty_add_word":empty,"n_words": len(A2)}

def ours() -> dict:
    n = n_suffix_links("aba")
    empty = "raised"
    try:
        n_suffix_links("")
        empty = "accepted"
    except ValueError:
        pass
    return {"n_suffix_links": n, "empty": empty}

def main() -> int:
    rec = {"schema":"suffixlock.show_ahocorasick.v1","used":"https://github.com/WojciechMula/pyahocorasick","built":"suffix-link occupancy 3 on aba; empty text is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["n_suffix_links"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("suffixlock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
