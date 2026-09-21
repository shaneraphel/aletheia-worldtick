import pytest
from aviation_legs.store import LEGS, register


def test_requires_key():
    LEGS.clear()
    with pytest.raises(ValueError):
        register("bos-jfk")


def test_binds_key():
    LEGS.clear()
    register("bos-jfk", flight_id="f-a")
    register("jfk-sfo", flight_id="f-b")
    assert [row["route"] for row in LEGS["f-a"]] == ["bos-jfk"]
    assert [row["route"] for row in LEGS["f-b"]] == ["jfk-sfo"]
