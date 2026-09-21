import pytest
from openapi_specs.store import SPECS, register


def test_requires_key():
    SPECS.clear()
    with pytest.raises(ValueError):
        register('/openapi.json')


def test_binds_key():
    SPECS.clear()
    register('/openapi.json', openapi_id='o-a')
    register('/v2/openapi.json', openapi_id='o-b')
    assert [row["href"] for row in SPECS["o-a"]] == ['/openapi.json']
    assert [row["href"] for row in SPECS["o-b"]] == ['/v2/openapi.json']
