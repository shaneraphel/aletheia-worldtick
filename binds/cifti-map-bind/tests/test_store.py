import pytest
from cifti_maps.store import MAPS, register


def test_requires_key():
    MAPS.clear()
    with pytest.raises(ValueError):
        register('dconn')


def test_binds_key():
    MAPS.clear()
    register('dconn', cifti_id='c-a')
    register('dtseries', cifti_id='c-b')
    assert [row["dconn"] for row in MAPS["c-a"]] == ['dconn']
    assert [row["dconn"] for row in MAPS["c-b"]] == ['dtseries']
