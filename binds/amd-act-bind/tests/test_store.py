import pytest
from amd_act.store import KERNELS, register


def test_requires_key():
    KERNELS.clear()
    with pytest.raises(ValueError):
        register("gemm")


def test_binds_key():
    KERNELS.clear()
    register("gemm", act_id="a-a")
    register("conv", act_id="a-b")
    assert [row["op"] for row in KERNELS["a-a"]] == ["gemm"]
    assert [row["op"] for row in KERNELS["a-b"]] == ["conv"]
