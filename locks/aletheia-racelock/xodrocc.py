"""OpenDRIVE occupancy. An empty road network is absence, not 0 roads.

ASAM OpenDRIVE names roads and successor links. Zero <road> elements refuse.
"""
from __future__ import annotations

import re
from pathlib import Path

Z = -1


def write_opendrive(path, nxt):
    if nxt is None or not nxt:
        raise ValueError("uncompiled OpenDRIVE network is absence")
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    roads = []
    for i, succ in enumerate(nxt):
        roads.append(
            f'<road name="r{i}" length="10" id="{i}" junction="-1">'
            f'<link><successor elementType="road" elementId="{int(succ)}" contactPoint="start"/></link>'
            f'<planView><geometry s="0" x="{i * 10}" y="0" hdg="0" length="10"><line/></geometry></planView>'
            f'<lanes><laneSection s="0"><center><lane id="0" type="none" level="false"/></center>'
            f'<right><lane id="-1" type="driving" level="false"/></right></laneSection></lanes>'
            f"</road>"
        )
    dest.write_text(
        '<?xml version="1.0"?>\n<OpenDRIVE>\n'
        '<header revMajor="1" revMinor="4" name="lane" version="1.00" '
        'date="2026-09-19" north="0" south="0" east="0" west="0"/>\n'
        + "\n".join(roads)
        + "\n</OpenDRIVE>\n"
    )
    return dest


def read_opendrive(path):
    text = Path(path).read_text() if Path(path).exists() else ""
    if "<OpenDRIVE" not in text:
        raise ValueError("uncompiled OpenDRIVE network is absence")
    ids = re.findall(r'<road[^>]*\bid="(\d+)"', text)
    succs = re.findall(r'<successor[^>]*elementId="(\d+)"', text)
    if not ids or len(succs) != len(ids):
        raise ValueError("uncompiled OpenDRIVE network is absence")
    nxt = [0] * len(ids)
    for i, sid in enumerate(ids):
        nxt[int(sid)] = int(succs[i])
    return nxt


def opendrive_occupancy(path):
    return len(read_opendrive(path))
