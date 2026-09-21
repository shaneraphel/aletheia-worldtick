import pytest
from airflow_plugin.store import PLUGINS, register


def test_requires_key():
    PLUGINS.clear()
    with pytest.raises(ValueError):
        register("hook-a")


def test_binds_key():
    PLUGINS.clear()
    register("hook-a", plugin_id="p-a")
    register("hook-b", plugin_id="p-b")
    assert [row["hook"] for row in PLUGINS["p-a"]] == ["hook-a"]
    assert [row["hook"] for row in PLUGINS["p-b"]] == ["hook-b"]
