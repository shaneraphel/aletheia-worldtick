from hip_interval.scale import scale


def test_requires_interval():
    assert scale(2.0, 3.0, interval=True) == 6.0


def test_binds_point():
    assert scale(2.0, 3.0, interval=False) == 6.0 + 273.15
