import pytest
from airflow_dags.store import DAGS, queue


def test_requires_key():
    DAGS.clear()
    with pytest.raises(ValueError):
        queue("x")


def test_binds_key():
    DAGS.clear()
    queue("a", dag_id="k-a")
    queue("b", dag_id="k-b")
    assert [row["op"] for row in DAGS["k-a"]] == ["a"]
    assert [row["op"] for row in DAGS["k-b"]] == ["b"]
