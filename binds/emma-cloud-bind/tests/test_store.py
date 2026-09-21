import pytest
from emma_cloud.store import NODES, register


def test_requires_key():
    NODES.clear()
    with pytest.raises(ValueError):
        register("h100")


def test_binds_key():
    NODES.clear()
    register("h100", cloud_id="c-a")
    register("b300", cloud_id="c-b")
    assert [row["shape"] for row in NODES["c-a"]] == ["h100"]
    assert [row["shape"] for row in NODES["c-b"]] == ["b300"]
