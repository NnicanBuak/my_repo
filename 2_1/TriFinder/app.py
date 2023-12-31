# Python >3.10

from pycoordsplain.points import Point, PointsDraw
from pycoordsplain.triangles import Triangle, TrianglesDraw

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.pyplot import text
from matplotlib.widgets import Button, TextBox

import threading
from itertools import permutations
import uuid
import re


def read_pointlist_from_file(file_path: str) -> str | None:
    try:
        with open(file_path) as pointlist:
            points.list = []
            for point_coordinates in re.findall(r"\[\d{1,}, \d{1,}]", pointlist.read()):
                point_coordinates_list = point_coordinates.strip("[]").split(",")
                points.add_point_with_coordinates(
                    int(point_coordinates_list[0]), int(point_coordinates_list[1])
                )
            points.update_draw()

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return "File not found."
    except PermissionError:
        print(f"Error: Permission denied while trying to open {file_path}.")
        return "Error: Permission denied while trying to open file."
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
        return "An unexpected error occurred"


def triangles_area_map(points: list[Point]):
    triangles_area_map: dict[Triangle, float] = {}

    n: int = len(points)
    predicted_triangles_count: int = n * (n - 1) * (n - 2)

    progress_text.set_text("0%")
    setted_progress: float = 0.0
    for count, combo in enumerate(permutations(points, 3), 1):
        current_triangle: Triangle = Triangle(f"temp-{uuid.uuid4()}", *combo)
        area: float = current_triangle.area

        progress: float = round(count / predicted_triangles_count * 100, 1)
        if progress > setted_progress:
            progress_text.set_text(f"{progress:.1f}%")
            setted_progress = progress
        if current_triangle.valid:
            triangles_area_map[current_triangle] = area
        else:
            print(
                f"not valid Triangle: {current_triangle.point1.number}, {current_triangle.point2.number}, {current_triangle.point3.number}"
            )
    progress_text.set_text("")
    return triangles_area_map


def min_max_triangle(
    triangles_area: dict[Triangle, float]
) -> tuple[Triangle, Triangle]:
    return min(set(triangles_area), key=triangles_area.get), max(set(triangles_area), key=triangles_area.get)  # type: ignore


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


def on_findbutton_clicked(event) -> None:
    global min_triangle, max_triangle
    with thread_creation_lock:
        if threading.active_count() > 1:
            return

        process = threading.Thread(
            target=calculating_triangles_process, args=(points.list,)
        )
        triangles.list = []
        triangles.update_draw()
        process.start()
        while process.is_alive():
            figure.canvas.draw()
            plt.pause(0.1)
        process.join(timeout=120)
        if process.is_alive():
            print("Process timeout, try again")
        else:
            triangles.add_triangle_with_points(
                "min", min_triangle.point1, min_triangle.point2, min_triangle.point3  # type: ignore
            )
            triangles.add_triangle_with_points(
                "max", max_triangle.point1, max_triangle.point2, max_triangle.point3  # type: ignore
            )
            print(f"min area: {min_triangle.area}, max area: {max_triangle.area}")  # type: ignore


def calculating_triangles_process(points):
    global min_triangle, max_triangle
    try:
        triangles_area: dict[Triangle, float] = triangles_area_map(points)
        min_triangle, max_triangle = min_max_triangle(triangles_area)
    except Exception as e:
        print(f"Error in calculating_process: {e}")


# print(plt.style.available)
plt.style.use("seaborn-v0_8-darkgrid")
# print(matplotlib.rcParams.keys())
plt.rcParams["figure.figsize"] = (7, 7)

figure, axes = plt.subplots()
axes.set_title("Coordinate plane")
axes.set_xlabel("X-axis")
axes.set_ylabel("Y-axis")
progress_text = figure.text(0.99, 0.965, "", horizontalalignment="right")
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
triangles = TrianglesDraw(axes, mcolors.CSS4_COLORS["orange"], points_scale=3)

pointlist_input_buffer: str = pointlist_input.text
exception: str | None = read_pointlist_from_file(pointlist_input.text)
if exception:
    inputresponse_text.set_color("r")
    inputresponse_text.set_text(exception)
    pointlist_input.set_val(pointlist_input_buffer)
else:
    inputresponse_text.set_color("g")
    inputresponse_text.set_text("Done")

points.adjust_axis_limits()

min_triangle, max_triangle = None, None
thread_creation_lock = threading.Lock()

plt.show()
