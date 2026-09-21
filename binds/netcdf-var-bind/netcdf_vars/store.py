"""A NetCDF leftover: every variable lands in one unsigned list."""

from __future__ import annotations

VARS: dict[str, list] = {}


def register(var, netcdf_id: str | None = None) -> None:
    if not netcdf_id:
        raise ValueError("netcdf var requires a netcdf id")
    VARS.setdefault(netcdf_id, []).append({"var": var})
