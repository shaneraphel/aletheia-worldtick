import pytest
from airflow_llm.store import BRANCHES, register


def test_requires_key():
    BRANCHES.clear()
    with pytest.raises(ValueError):
        register("ask")


def test_binds_key():
    BRANCHES.clear()
    register("ask", llm_id="m-a")
    register("branch", llm_id="m-b")
    assert [row["prompt"] for row in BRANCHES["m-a"]] == ["ask"]
    assert [row["prompt"] for row in BRANCHES["m-b"]] == ["branch"]
