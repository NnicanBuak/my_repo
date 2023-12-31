from .points import Point


from matplotlib.tri import Triangulation

import numpy as np
import re

class Triangle:
    def __init__(self, id: str, point1: Point, point2: Point, point3: Point) -> None:
        self.id: str = id
        self.point1: Point = point1
        self.point2: Point = point2
        self.point3: Point = point3
        self.valid: bool = self.check_validity()

    def check_validity(self) -> bool:
        points = [self.point1, self.point2, self.point3]
        return (points[1].y - points[0].y) * (points[2].x - points[1].x) != (
            points[2].y - points[1].y
        ) * (points[1].x - points[0].x)

    @property
    def points(self) -> tuple[Point, Point, Point]:
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
    def __init__(self, axes, color, points_scale: int = 3) -> None:
        self.triangleCount = 1
        self.axes = axes
        self.color = color
        self.scale: int = points_scale
        self.list: list[Triangle] = []

        self.draw = None
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

    def add_triangle(self, triangle: Triangle) -> None:
        if triangle.id in [triangle.id for triangle in self.list]:
            raise ValueError(f"A point with {triangle.id} id already exists")

        if triangle.valid:
            self.list.append(triangle)
            self.update_draw()

    def add_triangle_with_points(
        self, id: str, point1: Point, point2: Point, point3: Point
    ) -> None:
        triangle = Triangle(id, point1, point2, point3)
        if triangle.valid:
            self.list.append(triangle)
            self.update_draw()

    def remove_triangle_by_id(self, id: str) -> None:
        for triangle in self.list:
            if triangle.id == id:
                self.list.remove(triangle)
                self.update_draw()
                break

    def remove_triangles_by_id_pattern(self, id_pattern: str) -> None:
        self.list = [triangle for triangle in self.list if re.match(id_pattern, triangle.id)]
        self.update_draw()

    def on_triangle(self, x, y) -> Triangle | None:
        if not self.list:
            return None

        return min(
            self.list,
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

    def update_draw(self) -> None:
        if not self.list:
            if hasattr(self, "draw_lines") and hasattr(self, "draw_markers"):
                for line in self.draw_lines.get_children():
                    line.remove()
                for marker in self.draw_markers.get_children():
                    marker.remove()

            self.axes.figure.canvas.flush_events()
            self.axes.figure.canvas.draw_idle()

            # Установка self.draw в None
            self.draw = None

            return

        combined_x = np.concatenate(
            [[tri.point1.x, tri.point2.x, tri.point3.x] for tri in self.list]
        )
        combined_y = np.concatenate(
            [[tri.point1.y, tri.point2.y, tri.point3.y] for tri in self.list]
        )
        # print(combined_x)
        # print(combined_y)
        if self.draw is None:
            combined_triangles = list(np.arange(len(combined_x)).reshape(-1, 3))

            combined_triangulation = Triangulation(combined_x, combined_y, combined_triangles)
            self.draw_lines, self.draw_markers = self.axes.triplot(
                combined_triangulation,
                marker="o",
                markersize=self.scale,
                linestyle="-",
                c=self.color,
            )
        else:
            pass

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
        triangle_points = [triangle.point1, triangle.point2, triangle.point3]
        self.annotation.xy = (
            min(point.x for point in triangle_points),
            min(point.y for point in triangle_points),
        )
        self.annotation.set_text(
            f"Triangle {triangle.id} area: {triangle.area}\nP{triangle.point1.number}[{triangle.point1.x:.0f}, {triangle.point1.y:.0f}], P{triangle.point2.number}[{triangle.point2.x:.0f}, {triangle.point2.y:.0f}], P{triangle.point3.number}[{triangle.point3.x:.0f}, {triangle.point3.y:.0f}]"
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