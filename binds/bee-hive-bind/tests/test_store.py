import pytest
from bee_hives.store import HIVES, log


def test_requires_key():
    HIVES.clear()
    with pytest.raises(ValueError):
        log("x")


def test_binds_key():
    HIVES.clear()
    log("a", hive_id="k-a")
    log("b", hive_id="k-b")
    assert [row["note"] for row in HIVES["k-a"]] == ["a"]
    assert [row["note"] for row in HIVES["k-b"]] == ["b"]
