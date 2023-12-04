from matplotlib.axes import Axes
from pycoordsplain.points import Point, PointsDraw
from pycoordsplain.triangles import Triangle, TrianglesDraw, min_max_triangle


from matplotlib.widgets import Button, TextBox
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation


def read_pointslist_from_file(file_path: str):
    try:
        with open(file_path) as pointlist:
            # "[0, 1][2, 5][3, 0]"" ...
            points.list = []
            splitted_pointlist: list[str] = pointlist.read().strip("[]").split("][")
            for splitted_point in splitted_pointlist:
                points.add_point(
                    int(splitted_point.split(",")[0]), int(splitted_point.split(",")[1])
                )
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return FileNotFoundError
    except PermissionError:
        print(f"Error: Permission denied while trying to open {file_path}.")
        return PermissionError
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
        return e

def distance_squared(point1, point2):
    return (point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2


def on_findbutton_clicked(event) -> None:
    min_max_triangle(points.list)

def on_pointlistpath_submit(event) -> None:
    global pointslist_input_buffer
    exception = read_pointslist_from_file(event)
    if exception:
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
    figure.suptitle("\n\nЗадача: Поиск max и min треугольников между заданными точками")
    axes.set_title("Координатная плоскость")
    axes.set_xlabel("Ось X")
    axes.set_ylabel("Ось Y")
    find_button = Button(plt.axes((0.9, 0.95, 0.1, 0.05)), "Поиск", color="g")
    find_button.on_clicked(on_findbutton_clicked)
    pointslist_input = TextBox(plt.axes((0.18, 0.95, 0.3, 0.05)), "Путь к списку точек:", "./2_1/data/plist.txt")
    pointslist_input.on_submit(on_pointlistpath_submit)

    pointslist_input_buffer: str = pointslist_input.text

    points = PointsDraw(axes, scale=10)

    read_pointslist_from_file(pointslist_input.text)

    points.adjust_axis_limits()
    plt.show()
