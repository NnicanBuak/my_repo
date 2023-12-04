from matplotlib.axes import Axes
from pycoordsplain.points import Point, PointsDraw
from pycoordsplain.triangles import Triangle, TrianglesDraw, min_max_triangle


from matplotlib.widgets import Button
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation


def distance_squared(point1, point2):
    return (point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2


def on_clicked(event):
    min_max_triangle(points.list)


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
    button = Button(plt.axes((0.9, 0.95, 0.1, 0.05)), "Поиск", color="g")
    button.on_clicked(on_clicked)

    points = PointsDraw(axes, scale=10)

    data_path: str = "./2_1/data/plist.txt"
    # data_path_input: str = input("Введите путь к файлу с координатами точек: ")
    # if data_path_input:
    #     data_path = data_path_input
    with open(data_path) as pointlist:
        # "[0, 1][2, 5][3, 0]"" ...
        splitted_pointlist: list[str] = pointlist.read().strip("[]").split("][")
        for splitted_point in splitted_pointlist:
            points.add_point(
                int(splitted_point.split(",")[0]), int(splitted_point.split(",")[1])
            )

    points.adjust_axis_limits()
    plt.show()
