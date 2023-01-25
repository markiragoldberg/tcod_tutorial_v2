from attrs import Factory, define

from lerp import lerp_xy


@define
class SimpleCurve:
    """An approximation of an arbitrary curve created by
    linearly interpolating (drawing lines) between reference points.
    Class instances are callable to evaluate the curve at a given point.

    Raises:
        Exception: Raised when attempting to evaluate
        a curve with no points defined.
    """

    _points: list[tuple[float, float]] = Factory(list)

    def add_point(self, point: tuple[float, float]) -> None:
        """Add a point to the SimpleCurve.

        Args:
            point (tuple[float, float]): The new point on the curve,
            as a tuple of the form (input x, output y).
        """
        self._points.append(point)
        self._points.sort(key=lambda pt: pt[0])

    def __call__(self, n: float) -> float:
        """Find point (n, y) on the curve and returns y.
        If n is outside the curve's input range, the closest
        value in the curve's range will be used instead of n.

        Args:
            n (float): the input x-value whose output you want.

        Raises:
            Exception: Raised if the curve cannot be evaluated,
            as it has no points.

        Returns:
            float: the output y-value for point (n, y).
        """
        if len(self._points) == 0:
            raise Exception("Attempted to evaluate a simple curve with no points")
        # if curve has only one point return that point's y
        if len(self._points) == 1:
            return self._points[0][1]
        # if input is out of bounds, return the nearest bound's y
        if n < self._points[0][0]:
            return self._points[0][1]
        if n > self._points[-1][0]:
            return self._points[-1][1]

        # find bounding points
        i = 1
        while n > self._points[i][0]:
            i += 1

        # obtain the output using lerp
        pt1 = self._points[i - 1]
        pt2 = self._points[i]
        return lerp_xy(pt1[0], pt2[0], pt1[1], pt2[1], n)
