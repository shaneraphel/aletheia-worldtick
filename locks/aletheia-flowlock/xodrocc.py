"""OpenDRIVE junction occupancy. An empty road network is absence, not 0 roads.

ASAM OpenDRIVE junctions name incoming-to-connecting links. Road length is
the unit capacity on that connecting road. Zero connections refuse.
"""
from __future__ import annotations

import re
from pathlib import Path

Z = -1


def write_opendrive_junction(path, graph, lengths=None):
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
        ln = 10 if lengths is None else int(lengths[i])
        if ln < 1:
            raise ValueError("uncompiled OpenDRIVE network is absence")
        roads.append(
            f'<road name="r{i}" length="{ln}" id="{i}" junction="-1">'
            f'<planView><geometry s="0" x="{i * 10}" y="0" hdg="0" length="{ln}"><line/></geometry></planView>'
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
        '<header revMajor="1" revMinor="4" name="flow" version="1.00" '
        'date="2026-09-19" north="0" south="0" east="0" west="0"/>\n'
        + "\n".join(roads)
        + '\n<junction name="j0" id="0">\n'
        + "\n".join(conns)
        + "\n</junction>\n</OpenDRIVE>\n"
    )
    return dest


def _road_lengths(text):
    lengths = {}
    for m in re.finditer(r"<road\b[^>]*>", text):
        tag = m.group(0)
        rid = re.search(r'\bid="(\d+)"', tag)
        ln = re.search(r'\blength="([0-9.]+)"', tag)
        if rid and ln:
            lengths[int(rid.group(1))] = int(float(ln.group(1)))
    return lengths


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


def read_opendrive_weighted(path):
    text = Path(path).read_text() if Path(path).exists() else ""
    graph = read_opendrive_junction(path)
    lengths = _road_lengths(text)
    weighted = []
    for i, succs in enumerate(graph):
        for j in succs:
            w = lengths.get(j, 0)
            if w < 1:
                raise ValueError("uncompiled OpenDRIVE network is absence")
            weighted.append((i, j, w))
    if not weighted:
        raise ValueError("uncompiled OpenDRIVE network is absence")
    return weighted


def opendrive_occupancy(path):
    return len(read_opendrive_junction(path))
