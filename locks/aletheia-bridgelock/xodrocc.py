"""OpenDRIVE junction occupancy. An empty road network is absence, not 0 roads.

ASAM OpenDRIVE junctions name incoming-to-connecting links. Zero connections refuse.
"""
from __future__ import annotations

import re
from pathlib import Path

Z = -1


def write_opendrive_junction(path, graph):
    if graph is None or not graph:
        raise ValueError("uncompiled OpenDRIVE network is absence")
    edges = []
    for i, succs in enumerate(graph):
        if succs is None:
            raise ValueError("uncompiled OpenDRIVE network is absence")
        for s in succs:
            edges.append((i, int(s)))
    if not edges:
        raise ValueError("uncompiled OpenDRIVE network is absence")
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    roads = []
    for i in range(len(graph)):
        roads.append(
            f'<road name="r{i}" length="10" id="{i}" junction="-1">'
            f'<planView><geometry s="0" x="{i * 10}" y="0" hdg="0" length="10"><line/></geometry></planView>'
            f'<lanes><laneSection s="0"><center><lane id="0" type="none" level="false"/></center>'
            f'<right><lane id="-1" type="driving" level="false"/></right></laneSection></lanes>'
            f"</road>"
        )
    conns = []
    for cid, (a, b) in enumerate(edges):
        conns.append(
            f'<connection id="{cid}" incomingRoad="{a}" connectingRoad="{b}" contactPoint="start"/>'
        )
    dest.write_text(
        '<?xml version="1.0"?>\n<OpenDRIVE>\n'
        '<header revMajor="1" revMinor="4" name="tour" version="1.00" '
        'date="2026-09-19" north="0" south="0" east="0" west="0"/>\n'
        + "\n".join(roads)
        + '\n<junction name="j0" id="0">\n'
        + "\n".join(conns)
        + "\n</junction>\n</OpenDRIVE>\n"
    )
    return dest


def read_opendrive_junction(path):
    text = Path(path).read_text() if Path(path).exists() else ""
    if "<OpenDRIVE" not in text or "<junction" not in text:
        raise ValueError("uncompiled OpenDRIVE network is absence")
    edges = []
    for m in re.finditer(r"<connection\b[^>]*>", text):
        tag = m.group(0)
        inc = re.search(r'incomingRoad="(\d+)"', tag)
        con = re.search(r'connectingRoad="(\d+)"', tag)
        if inc and con:
            edges.append((int(inc.group(1)), int(con.group(1))))
    if not edges:
        raise ValueError("uncompiled OpenDRIVE network is absence")
    n = 1 + max(max(a, b) for a, b in edges)
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
    if not any(graph):
        raise ValueError("uncompiled OpenDRIVE network is absence")
    return graph


def opendrive_occupancy(path):
    return len(read_opendrive_junction(path))
