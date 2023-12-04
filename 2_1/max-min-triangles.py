from pycoordsplain.points import Point, PointsDraw
from pycoordsplain.triangles import Triangle, TrianglesDraw

from itertools import permutations

import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation


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


if __name__ == "__main__":
    # print(plt.style.available)
    plt.style.use("seaborn-v0_8-darkgrid")
    # print(matplotlib.rcParams.keys())
    plt.rcParams["figure.figsize"] = (8, 8)

    figure, axes = plt.subplots()
    figure.suptitle("Задача: Поиск max и min треугольников между заданными точками")
    axes.set_title("Координатная плоскость")
    axes.set_xlabel("Ось X")
    axes.set_ylabel("Ось Y")

    points = PointsDraw(axes, scale=10)

    data_path: str = "./2_1/data/plist.txt"
    data_path_input: str = input("Введите путь к файлу с координатами точек: ")
    if data_path_input:
        data_path = data_path_input
    with open(data_path) as pointlist:
        # "[0, 1][2, 5][3, 0]"" ...
        splitted_pointlist: list[str] = pointlist.read().strip("[]").split("][")
        for splitted_point in splitted_pointlist:
            points.add_point(
                int(splitted_point.split(",")[0]), int(splitted_point.split(",")[1])
            )

    points.adjust_axis_limits()
    plt.show()
