import unittest
import time

from pycoordsplain.points import Point
from pycoordsplain.triangles import Triangle


class Item:
    def __init__(self, id) -> None:
        self.id = id
        pass


class TriangleTestCase(unittest.TestCase):
    def testTriangleArea1(self):
        triangle = Triangle(
            "test1", Point(0, x=0, y=0), Point(1, x=0, y=1), Point(2, x=1, y=0)
        )
        if triangle.area == 0.5: print("Area1 passed")

    def testTriangleArea2(self):
        triangle = Triangle(
            "test1", Point(0, x=1, y=5), Point(1, x=4, y=6), Point(2, x=0, y=7)
        )
        if triangle.area == 0.5: print("Area2 passed")

    def testTriangleArea3(self):
        triangle = Triangle(
            "test1", Point(0, x=34, y=26), Point(1, x=34, y=25), Point(2, x=35, y=25)
        )
        if triangle.area == 0.5: print("Area3 passed")


class RemoveListItemTestCaseGeneratingNewList1(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t))

    def testListRemovingById(self):
        _list = [Item(id) for id in range(10_000_000)]
        _list = [triangle for triangle in _list if triangle.id != id]

class RemoveListItemTestCaseGeneratingNewList2(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t))

    def testListRemovingById(self):
        _list = [Item(id) for id in reversed(range(10_000_000))]
        _list = [triangle for triangle in _list if triangle.id != id]

class RemoveListItemTestCaseRemovingFindedItemInList1(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t))

    def testListRemovingById(self):
        _list = [Item(id) for id in range(10_000_000)]
        for triangle in _list:
            if triangle.id == id:
                _list.remove(triangle)
                break

class RemoveListItemTestCaseRemovingFindedItemInList2(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t))

    def testListRemovingById(self):
        _list = [Item(id) for id in reversed(range(10_000_000))]
        for triangle in _list:
            if triangle.id == id:
                _list.remove(triangle)
                break


if __name__ == "__main__":
    unittest.main()
