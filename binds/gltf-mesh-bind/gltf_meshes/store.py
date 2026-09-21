"""A glTF leftover: every mesh lands in one unsigned list."""

from __future__ import annotations

MESHES: dict[str, list] = {}


def register(prim, gltf_id: str | None = None) -> None:
    if not gltf_id:
        raise ValueError("gltf mesh requires a gltf id")
    MESHES.setdefault(gltf_id, []).append({"prim": prim})
