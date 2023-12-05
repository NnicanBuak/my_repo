# Python >3.10

from pycoordsplain.points import Point, PointsDraw
from pycoordsplain.triangles import Triangle, TrianglesDraw, min_max_triangle


import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from matplotlib.widgets import Button, TextBox
from matplotlib.tri import Triangulation

import re


def read_pointslist_from_file(file_path: str) -> str | None:
    try:
        with open(file_path) as pointlist:
            points.list = []
            for point_coordinates in re.findall(r"\[\d{1,}, \d{1,}]", pointlist.read()):
                point_coordinates_list = point_coordinates.strip("[]").split(",")
                points.add_point(
                    int(point_coordinates_list[0]), int(point_coordinates_list[1])
                )

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return "File not found."
    except PermissionError:
        print(f"Error: Permission denied while trying to open {file_path}.")
        return "Error: Permission denied while trying to open file."
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
        return "An unexpected error occurred"


def distance_squared(point1: Point, point2: Point) -> int:
    return (point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2


def on_findbutton_clicked(event) -> None:
    min_max_triangle(points.list)


def on_pointlistpath_submit(event) -> None:
    global pointslist_input_buffer
    exception = read_pointslist_from_file(event)
    if exception:
        error_text.set_text(exception)
        pointslist_input.set_val(pointslist_input_buffer)
        return
    pointslist_input_buffer = event
    points.update_draw()


if __name__ == "__main__":
    # print(plt.style.available)
    plt.style.use("seaborn-v0_8-darkgrid")
    # print(matplotlib.rcParams.keys())
    plt.rcParams["figure.figsize"] = (8, 8)

    figure, axes = plt.subplots()
    axes.set_title("Coordinate plane")
    axes.set_xlabel("X-axis")
    axes.set_ylabel("Y-axis")
    find_button = Button(plt.axes((0.9, 0.95, 0.1, 0.05)), "Поиск", color="g")
    find_button.on_clicked(on_findbutton_clicked)
    pointslist_input = TextBox(
        plt.axes((0.18, 0.95, 0.3, 0.05)),
        "Путь к списку точек:",
        "./2_1/data/plist.txt",
    )
    pointslist_input.on_submit(on_pointlistpath_submit)
    error_text = text(0, -0.4, "")
    error_text.set_color("r")

    pointslist_input_buffer: str = pointslist_input.text

    points = PointsDraw(axes, scale=10)

    read_pointslist_from_file(pointslist_input.text)

    points.adjust_axis_limits()
    plt.show()
