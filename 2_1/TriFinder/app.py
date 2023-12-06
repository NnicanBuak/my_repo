# Python >3.10

from pycoordsplain.points import PointsDraw
from pycoordsplain.triangles import TrianglesDraw, min_max_triangle


import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.pyplot import text
from matplotlib.widgets import Button, TextBox

import re


def read_pointlist_from_file(file_path: str) -> str | None:
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


def on_findbutton_clicked(event) -> None:
    min_triangle, max_triangle = min_max_triangle(points.list)
    triangles.list = []
    triangles.add_triangle(
        "min", min_triangle.point1, min_triangle.point2, min_triangle.point3
    )
    triangles.add_triangle(
        "max", max_triangle.point1, max_triangle.point2, max_triangle.point3
    )


def on_pointlistpath_submit(event) -> None:
    global pointlist_input_buffer
    exception = read_pointlist_from_file(event)
    if exception:
        inputresponse_text.set_color("r")
        inputresponse_text.set_text(exception)
        pointlist_input.set_val(pointlist_input_buffer)
    elif event != pointlist_input_buffer:
        inputresponse_text.set_color("g")
        inputresponse_text.set_text("Done")
        pointlist_input_buffer = event
        points.update_draw()


if __name__ == "__main__":
    # print(plt.style.available)
    plt.style.use("seaborn-v0_8-darkgrid")
    # print(matplotlib.rcParams.keys())
    plt.rcParams["figure.figsize"] = (6, 6)

    figure, axes = plt.subplots()
    axes.set_title("Coordinate plane")
    axes.set_xlabel("X-axis")
    axes.set_ylabel("Y-axis")
    find_button = Button(
        plt.axes((0.6, 0.95, 0.3, 0.05)),
        "Find min/max Triangles",
        color=mcolors.CSS4_COLORS["lightgreen"],
        hovercolor=mcolors.CSS4_COLORS["palegreen"],
    )
    find_button.on_clicked(on_findbutton_clicked)
    pointlist_input = TextBox(
        plt.axes((0.15, 0.95, 0.3, 0.05)),
        "Path:",
        "./2_1/data/plist.txt",
        hovercolor=mcolors.CSS4_COLORS["whitesmoke"],
    )
    pointlist_input.on_submit(on_pointlistpath_submit)
    inputresponse_text = text(0, -0.5, "")

    points = PointsDraw(axes, mcolors.CSS4_COLORS["slategray"], scale=6)
    triangles = TrianglesDraw(axes, mcolors.CSS4_COLORS["orange"], points_scale=8)

    pointlist_input_buffer: str = pointlist_input.text
    exception = read_pointlist_from_file(pointlist_input.text)
    if exception:
        inputresponse_text.set_color("r")
        inputresponse_text.set_text(exception)
        pointlist_input.set_val(pointlist_input_buffer)
    else:
        inputresponse_text.set_color("g")
        inputresponse_text.set_text("Done")
    points.adjust_axis_limits()
    plt.show()
