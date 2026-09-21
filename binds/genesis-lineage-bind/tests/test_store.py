import pytest
from genesis_seeds.store import SEEDS, plant


def test_requires_key():
    SEEDS.clear()
    with pytest.raises(ValueError):
        plant("x")


def test_binds_key():
    SEEDS.clear()
    plant("a", lineage_id="k-a")
    plant("b", lineage_id="k-b")
    assert [row["prompt"] for row in SEEDS["k-a"]] == ["a"]
    assert [row["prompt"] for row in SEEDS["k-b"]] == ["b"]
