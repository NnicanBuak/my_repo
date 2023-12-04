if __name__ == "__main__":
    import importlib

    pycoordsplane = importlib.import_module("../max-min-triangles.py", "pycoordsplane")
    points = [
        pycoordsplane.Point(0, 0),
        pycoordsplane.Point(1, 0),
        pycoordsplane.Point(0, 1),
    ]
