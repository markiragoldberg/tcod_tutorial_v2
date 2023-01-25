import pytest

from simplecurve import SimpleCurve


def test_simplecurve_bad() -> None:
    curve = SimpleCurve()

    with pytest.raises(Exception) as e:
        curve(0)
    assert str(e.value) == "Attempted to evaluate a simple curve with no points"


def test_simplecurve_good() -> None:
    curve = SimpleCurve()

    curve.add_point((0, 0))
    assert curve(-1) == 0
    assert curve(0) == 0
    assert curve(1) == 0

    curve.add_point((10, 100))

    curve.add_point((5, 10))
    curve.add_point((100, 20))
    assert curve._points[1] == (5, 10)
    assert curve._points[2] == (10, 100)
    assert curve._points[3] == (100, 20)

    assert curve(-9999) == 0
    assert curve(0) == 0
    assert curve(2.5) == 5
    assert curve(5) == 10
    assert curve(7.5) == 55
    assert curve(10) == 100
    assert curve(55) == 60
    assert curve(100) == 20
    assert curve(9999) == 20
