from points import PointsDraw
from triangles import TrianglesDraw

import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation

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
