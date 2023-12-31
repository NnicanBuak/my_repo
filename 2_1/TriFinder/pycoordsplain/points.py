from typing import Literal
import numpy as np


class Point:
    def __init__(self, number: int, x: float, y: float) -> None:
        self.number: int = number
        self.x: float = x
        self.y: float = y


class PointsDraw:
    def __init__(
        self,
        axes,
        color,
        scale: int = 3,
    ) -> None:
        self.pointCount = 1
        self.axes = axes
        self.scale: int = scale
        self.list: list[Point] = []
        self.draw = self.axes.scatter([], [], s=scale, c=color)

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

    def add_point(self, point: Point) -> ValueError | None:
        if point.number in [point.number for point in self.list]:
            return ValueError(f"A point with {point.number} number already exists")
        self.pointCount += 1
        self.list.append(point)

    def add_point_with_coordinates(self, x: float, y: float) -> None:
        point = Point(self.pointCount, x, y)
        self.pointCount += 1
        self.list.append(point)

    def update_draw(self):
        coords: list[tuple[float, float]] = [(point.x, point.y) for point in self.list]
        self.draw.set_offsets(coords)
        self.adjust_axis_limits()
        self.axes.figure.canvas.draw_idle()

    def adjust_axis_limits(self) -> None:
        if not self.list:
            return

        x_values, y_values = zip(*[(point.x, point.y) for point in self.list])

        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)

        buffer = 5
        self.axes.set_xlim(x_min - buffer, x_max + buffer)
        self.axes.set_ylim(y_min - buffer, y_max + buffer)

    def on_point(self, x, y) -> Point | None:
        if not self.list:
            return

        valid_points = [
            point
            for point in self.list
            if np.sqrt((point.x - x) ** 2 + (point.y - y) ** 2) <= self.scale * 0.1
        ]

        return min(
            valid_points,
            key=lambda point: np.sqrt((point.x - x) ** 2 + (point.y - y) ** 2),
            default=None,
        )

    def on_hover(self, event) -> None:
        if (
            event.inaxes is not None
            and event.xdata is not None
            and event.ydata is not None
        ):
            point = self.on_point(event.xdata, event.ydata)
            if point:
                self.update_annotation(point)
                self.annotation.set_visible(True)
                self.axes.figure.canvas.draw_idle()
            else:
                self.annotation.set_visible(False)
                self.axes.figure.canvas.draw_idle()

    def on_leave(self, event) -> None:
        self.annotation.set_visible(False)
        self.axes.figure.canvas.draw_idle()

    def update_annotation(self, point):
        x, y = point.x, point.y
        self.annotation.xy = (x, y)
        self.annotation.set_text(f"Point {point.number}: [{x:.0f}, {y:.0f}]")
        self.axes.figure.canvas.draw_idle()
