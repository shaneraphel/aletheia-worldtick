from nemotron_kernel.gate import accept


def test_requires_exact_int():
    assert accept([1, 2], [1, 3]) is False


def test_binds_exact_int():
    assert accept([1, 2], [1, 2]) is True
