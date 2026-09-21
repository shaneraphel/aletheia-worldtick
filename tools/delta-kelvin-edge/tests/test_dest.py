import pytest
from delta_kelvin.convert import convert


def test_requires_kind():
    with pytest.raises(ValueError):
        convert(1.0, "interval", "point")


def test_binds_point():
    assert convert(1.0, "point", "kelvin") == 274.15
