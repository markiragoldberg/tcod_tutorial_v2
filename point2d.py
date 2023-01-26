from attrs import define


@define
class Point2d:
    """A point in two dimensions with an x and y coordinate."""
    x: int
    y: int
