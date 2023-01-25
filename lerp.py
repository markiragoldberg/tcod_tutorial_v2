""" Utility functions for generating arbitrary values on lines,
    given reference points.

    lerp_xy: General linear interpolation between two points.
    lerp_01: Linear interpolation between points x=0 and x=1.
    clamp_01: Restricts an input number to the range 0,1.
"""


def lerp_01(y1: float, y2: float, n: float) -> float:
    """A linear interpolation that assumes x1 is 0 and x2 is 1.
        For more information, read lerp_xy's docstring.

    Args:
        y1 (float): The result if n <= 0.0.
        y2 (float): The result if n >= 1.0.
        n (float): An x-value between 0-1 that determines the result.

    Returns:
        float: The y-value
    """
    return y1 + (y2 - y1) * clamp_01(n)


def clamp_01(n: float) -> float:
    """Returns the number from 0 to 1 that is closest to n,
        or n itself if 0 <= n <= 1.

    Args:
        n (float): A number.

    Returns:
        float: The number from 0-1 that is closest to n.
    """
    return max(min(n, 1.0), 0.0)


def lerp_xy(x1: float, x2: float, y1: float, y2: float, n: float) -> float:
    """Given a line (x1, y1) to (x2, y2),
       finds the point (n, y3) on that line,
       and returns y3.

    Args:
        x1 (float): the input value for the first reference point.
        x2 (float): the input value for the second reference point.
        y1 (float): the output value for the first reference point.
        y2 (float): the output value for the second reference point.
        n (float):  the input value you're actually interested in.

    Returns:
        float: the output value for your input value n.
    """
    percentage = (n - x1) / (x2 - x1)
    return y1 + (y2 - y1) * percentage
