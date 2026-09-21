import pytest
from airflow_hitl.store import APPROVALS, register


def test_requires_key():
    APPROVALS.clear()
    with pytest.raises(ValueError):
        register("approve")


def test_binds_key():
    APPROVALS.clear()
    register("approve", hitl_id="h-a")
    register("reject", hitl_id="h-b")
    assert [row["op"] for row in APPROVALS["h-a"]] == ["approve"]
    assert [row["op"] for row in APPROVALS["h-b"]] == ["reject"]
