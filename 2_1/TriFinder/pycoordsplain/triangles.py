from typing import Tuple
from .points import Point

from itertools import permutations


class Triangle:
    def __init__(self, id: str, point1: Point, point2: Point, point3: Point) -> None:
        self.id: str = id
        self.point1: Point = point1
        self.point2: Point = point2
        self.point3: Point = point3

    @property
    def points(self) -> Tuple[Point, Point, Point]:
        return (self.point1, self.point2, self.point3)

    @property
    def area(self) -> float:
        return 0.5 * abs(
            (
                self.point1.x * (self.point2.y - self.point3.y)
                + self.point2.x * (self.point3.y - self.point1.y)
                + self.point3.x * (self.point1.y - self.point2.y)
            )
        )


class TrianglesDraw:
    def __init__(self) -> None:
        pass


def min_max_triangle(points) -> tuple[Triangle, Triangle]:
    min_triangle = Triangle(
        "min", Point(0, x=0, y=0), Point(0, x=0, y=0), Point(0, x=0, y=0)
    )
    max_triangle = Triangle(
        "max", Point(0, x=0, y=0), Point(0, x=0, y=0), Point(0, x=0, y=0)
    )
    min_area: float = float("inf")
    max_area: float = 0.0

    for combo in permutations(points, 3):
        current_triangle = Triangle("min", *combo)
        area: float = current_triangle.area
        if area < min_area:
            min_area = area
            min_triangle: Triangle = current_triangle
        if area > max_area:
            max_area = area
            max_triangle: Triangle = current_triangle

    return min_triangle, max_triangle
