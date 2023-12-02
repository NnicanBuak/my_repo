from typing import Any, Literal, Tuple
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
import numpy as np


# print(plt.style.available)
plt.style.use("seaborn-v0_8-darkgrid")
# print(matplotlib.rcParams.keys())
plt.rcParams["figure.figsize"] = (8, 8)


class Point:
    def __init__(self, number: int, x: int, y: int) -> None:
        self.number: int = number
        self.x: int = x
        self.y: int = y


class Triangle:
    def __init__(self, points: Tuple[Point, Point, Point]) -> None:
        self.list: Tuple[Point, Point, Point] = points


class PointsScatter:
    def __init__(
        self,
        axes,
        scale: int = 1,
        color: Literal[
            "blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"
        ] = "black",
    ) -> None:
        colors = {
            "blue": "b",
            "green": "g",
            "red": "r",
            "cyan": "c",
            "magenta": "m",
            "yellow": "y",
            "black": "k",
            "white": "w",
        }
        self.pointCount = 1
        self.axes = axes
        self.scale: int = scale
        self.list: list[Point] = []
        self.scatter = self.axes.scatter([], [], s=scale, c=colors[color])

        self.annotation = self.axes.annotate(
            "",
            xy=(0, 0),
            xytext=(10, -20),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            # arrowprops=dict(arrowstyle="->"),
        )
        self.annotation.set_visible(False)

        self.axes.figure.canvas.mpl_connect("motion_notify_event", self.on_hover)
        self.axes.figure.canvas.mpl_connect("axes_leave_event", self.on_leave)

    def add_point(self, x, y):
        point = Point(self.pointCount, x, y)
        self.pointCount += 1
        self.list.append(point)
        self.update_scatter()

    def update_scatter(self):
        coords: list[tuple[int, int]] = [(point.x, point.y) for point in self.list]
        self.scatter.set_offsets(coords)
        self.axes.figure.canvas.draw_idle()

    def adjust_axis_limits(self):
        if not self.list:
            return

        x_values, y_values = zip(*[(point.x, point.y) for point in self.list])

        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)

        buffer = 5
        self.axes.set_xlim(x_min - buffer, x_max + buffer)
        self.axes.set_ylim(y_min - buffer, y_max + buffer)

    def on_hover(self, event):
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

    def on_leave(self, event):
        self.annotation.set_visible(False)
        self.axes.figure.canvas.draw_idle()

    def update_annotation(self, point):
        x, y = point.x, point.y
        self.annotation.xy = (x, y)
        self.annotation.set_text(f"Точка {point.number}: [{x:.0f}, {y:.0f}]")
        self.axes.figure.canvas.draw_idle()

    def on_point(self, x, y):
        if not self.list:
            return None

        for point in self.list:
            distance = np.sqrt((point.x - x) ** 2 + (point.y - y) ** 2)
            if distance <= self.scale*0.05:
                return point
        return None


if __name__ == "__main__":
    figure, axes = plt.subplots()
    figure.suptitle("Задача: Поиск max и min треугольников между заданными точками")
    axes.set_title("Координатная плоскость")
    axes.set_xlabel("Ось X")
    axes.set_ylabel("Ось Y")

    points = PointsScatter(axes, 10)

    with open("plist.txt") as pointlist:
        # "[0, 1][2, 5][3, 0]"" ...
        splitted_pointlist: list[str] = pointlist.read().strip("[]").split("][")
        for splitted_point in splitted_pointlist:
            points.add_point(
                int(splitted_point.split(",")[0]), int(splitted_point.split(",")[1])
            )
    points.adjust_axis_limits()
    plt.show()
