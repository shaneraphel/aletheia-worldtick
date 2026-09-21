import pytest
from vultr_rush.store import RUNS, register


def test_requires_key():
    RUNS.clear()
    with pytest.raises(ValueError):
        register("job-a")


def test_binds_key():
    RUNS.clear()
    register("job-a", rush_id="r-a")
    register("job-b", rush_id="r-b")
    assert [row["job"] for row in RUNS["r-a"]] == ["job-a"]
    assert [row["job"] for row in RUNS["r-b"]] == ["job-b"]
