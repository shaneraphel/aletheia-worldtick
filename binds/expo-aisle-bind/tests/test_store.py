import pytest
from expo_booth.store import BOOTHS, register


def test_requires_aisle():
    BOOTHS.clear()
    with pytest.raises(ValueError):
        register("team-a")


def test_binds_aisle():
    BOOTHS.clear()
    register("team-a", aisle="A1")
    register("team-b", aisle="B2")
    assert [row["team"] for row in BOOTHS["A1"]] == ["team-a"]
    assert [row["team"] for row in BOOTHS["B2"]] == ["team-b"]
