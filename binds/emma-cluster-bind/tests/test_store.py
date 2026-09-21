import pytest
from emma_probes.store import PROBES, ping


def test_requires_key():
    PROBES.clear()
    with pytest.raises(ValueError):
        ping("x")


def test_binds_key():
    PROBES.clear()
    ping("a", cluster_id="k-a")
    ping("b", cluster_id="k-b")
    assert [row["host"] for row in PROBES["k-a"]] == ["a"]
    assert [row["host"] for row in PROBES["k-b"]] == ["b"]
