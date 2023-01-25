# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from lerp import clamp_01, lerp_01, lerp_xy


def test_clamp01() -> None:
    assert clamp_01(-52.12) == 0.0
    assert clamp_01(0.0) == 0.0
    assert clamp_01(0.4287) == 0.4287
    assert clamp_01(1.0) == 1.0
    assert clamp_01(3910.124) == 1.0


def test_lerp_01() -> None:
    y1 = 20
    y2 = 200
    assert lerp_01(y1, y2, -129) == y1
    assert lerp_01(y1, y2, 0.0) == y1
    assert lerp_01(y1, y2, 0.25) == 0.25 * (y2 - y1) + y1
    assert lerp_01(y1, y2, 1.0) == y2
    assert lerp_01(y1, y2, 18324.178) == y2


def test_lerp_xy() -> None:
    x1 = 10
    x2 = 35
    y1 = 40
    y2 = 5000
    assert lerp_xy(x1, x2, y1, y2, x1 - 35) == y1
    assert lerp_xy(x1, x2, y1, y2, x1) == y1

    n = 22.3
    y_of_n = ((n - x1) / (x2 - x1)) * (y2 - y1) + y1
    assert lerp_xy(x1, x2, y1, y2, n) == y_of_n

    assert lerp_xy(x1, x2, y1, y2, x2) == y2
    assert lerp_xy(x1, x2, y1, y2, x2 + 91273) == y2
