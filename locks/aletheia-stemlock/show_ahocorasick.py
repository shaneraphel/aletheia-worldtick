#!/usr/bin/env python3.12
"""Use pyahocorasick on aba. Record empty needle. Refuse empty text here."""
from __future__ import annotations
import json, platform, sys
from ukkonen import n_suffix_links

def theirs() -> dict:
    import ahocorasick
    m = ahocorasick.Automaton()
    try:
        m.add_word("", 0)
        empty = "accepted"
    except Exception as exc:
        empty = f"{type(exc).__name__}: {exc}"
    m.add_word("ab", 1); m.add_word("ba", 2); m.make_automaton()
    return {"package":"pyahocorasick","version":__import__("importlib.metadata", fromlist=["version"]).version("pyahocorasick"),"empty_add_word":empty,"hits_aba":len(list(m.iter("aba")))}

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
    rec = {"schema":"stemlock.show_ahocorasick.v1","used":"https://github.com/WojciechMula/pyahocorasick","note":"https://github.com/WojciechMula/pyahocorasick/issues/225","built":"aba suffix-link occupancy 3; empty text is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["n_suffix_links"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("stemlock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
