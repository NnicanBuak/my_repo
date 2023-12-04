from typing import Any, Literal, Tuple
from itertools import permutations
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
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


class PointsDraw:
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
            if distance <= self.scale * 0.05:
                return point
        return None


def distance_squared(point1, point2):
    return (point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2


def find_min_max_triangle(points):
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


figure, axes = plt.subplots()
figure.suptitle("Задача: Поиск max и min треугольников между заданными точками")
axes.set_title("Координатная плоскость")
axes.set_xlabel("Ось X")
axes.set_ylabel("Ось Y")
button_ax = plt.axes((0.5 - 0.05, 0.909, 0.1, 0.05))  # left, bottom, width, height
button = Button(button_ax, "Поиск")

points = PointsDraw(axes, scale=10)

data_path: str = input("Введите путь к файлу с координатами точек: ")
with open(data_path) as pointlist:
    # "[0, 1][2, 5][3, 0]"" ...
    splitted_pointlist: list[str] = pointlist.read().strip("[]").split("][")
    for splitted_point in splitted_pointlist:
        points.add_point(
            int(splitted_point.split(",")[0]), int(splitted_point.split(",")[1])
        )

def find_triangles_event(event):
    min_triangle, max_triangle = find_min_max_triangle(points.list)
    print(
        [(point.x, point.y) for point in min_triangle.points],
        [(point.x, point.y) for point in max_triangle.points],
    )

button.on_clicked(find_triangles_event)
points.adjust_axis_limits()
plt.show()
