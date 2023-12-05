from typing import Tuple
from .points import Point

from itertools import permutations
import numpy as np


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
    def __init__(
        self,
        axes,
        color,
        points_scale: int = 3,
    ) -> None:
        self.triangleCount = 1
        self.axes = axes
        self.scale: int = points_scale
        self.list: list[Triangle] = []
        self.draw = self.axes.scatter([], [], s=points_scale, c=color)

        self.annotation = self.axes.annotate(
            "",
            xy=(0, 0),
            xytext=(10, -20),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
        )
        self.annotation.set_visible(False)

        self.axes.figure.canvas.mpl_connect("motion_notify_event", self.on_hover)
        self.axes.figure.canvas.mpl_connect("axes_leave_event", self.on_leave)

    def add_triangle(self, id: str, point1: Point, point2: Point, point3: Point) -> None:
        self.list.append(Triangle(id, point1, point2, point3))
        self.update_draw()

    def update_draw(self):
        coords: list[tuple[float, float]] = [
            (point.x, point.y) for triangle in self.list for point in triangle.points
        ]
        self.draw.set_offsets(coords)
        self.adjust_axis_limits()
        self.axes.figure.canvas.draw_idle()

    def adjust_axis_limits(self) -> None:
        if not self.list:
            return

        all_points = [point for triangle in self.list for point in triangle.points]
        x_values, y_values = zip(*[(point.x, point.y) for point in all_points])

        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)

        buffer = 5
        self.axes.set_xlim(x_min - buffer, x_max + buffer)
        self.axes.set_ylim(y_min - buffer, y_max + buffer)

    def on_triangle(self, x, y) -> Triangle | None:
        if not self.list:
            return None

        valid_triangles = [
            t
            for t in self.list
            if self.point_in_triangle(
                x,
                y,
                t.point1.x,
                t.point1.y,
                t.point2.x,
                t.point2.y,
                t.point3.x,
                t.point3.y,
            )
        ]

        return min(
            valid_triangles,
            key=lambda t: self.distance_to_triangle(
                x,
                y,
                t.point1.x,
                t.point1.y,
                t.point2.x,
                t.point2.y,
                t.point3.x,
                t.point3.y,
            ),
            default=None,
        )

    def on_hover(self, event) -> None:
        if (
            event.inaxes is not None
            and event.xdata is not None
            and event.ydata is not None
        ):
            triangle = self.on_triangle(event.xdata, event.ydata)
            if triangle:
                self.update_annotation(triangle)
                self.annotation.set_visible(True)
                self.axes.figure.canvas.draw_idle()
            else:
                self.annotation.set_visible(False)
                self.axes.figure.canvas.draw_idle()

    def on_leave(self, event) -> None:
        self.annotation.set_visible(False)
        self.axes.figure.canvas.draw_idle()

    def update_annotation(self, triangle):
        x1, y1, x2, y2, x3, y3 = (
            triangle.point1.x,
            triangle.point1.y,
            triangle.point2.x,
            triangle.point2.y,
            triangle.point3.x,
            triangle.point3.y,
        )
        self.annotation.xy = (x1, y1)
        self.annotation.set_text(
            f"Треугольник {triangle.id}: P1[{x1:.0f}, {y1:.0f}], P2[{x2:.0f}, {y2:.0f}], P3[{x3:.0f}, {y3:.0f}]"
        )
        self.axes.figure.canvas.draw_idle()

    @staticmethod
    def point_in_triangle(px, py, x1, y1, x2, y2, x3, y3) -> bool:
        d1 = TrianglesDraw.sign(px, py, x1, y1, x2, y2)
        d2 = TrianglesDraw.sign(px, py, x2, y2, x3, y3)
        d3 = TrianglesDraw.sign(px, py, x3, y3, x1, y1)
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        return not (has_neg and has_pos)

    @staticmethod
    def sign(px, py, x1, y1, x2, y2) -> float:
        return (px - x2) * (y1 - y2) - (x1 - x2) * (py - y2)

    @staticmethod
    def distance_to_triangle(px, py, x1, y1, x2, y2, x3, y3) -> float:
        return min(
            TrianglesDraw.point_to_line_distance(px, py, x1, y1, x2, y2),
            TrianglesDraw.point_to_line_distance(px, py, x2, y2, x3, y3),
            TrianglesDraw.point_to_line_distance(px, py, x3, y3, x1, y1),
        )

    @staticmethod
    def point_to_line_distance(px, py, x1, y1, x2, y2) -> float:
        num = np.abs((x2 - x1) * (y1 - py) - (x1 - px) * (y2 - y1))
        den = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return num / den


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
