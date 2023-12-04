import unittest

from pycoordsplain.points import Point
from pycoordsplain.triangles import Triangle

class TriangleTestCase(unittest.TestCase):
    def testTriangleArea1(self):
        triangle = (Triangle("test1", Point(0, x=0, y=0), Point(1, x=0, y=1), Point(2, x=1, y=0)))
        return triangle.area == 0.5
    def testTriangleArea2(self):
        triangle = (Triangle("test1", Point(0, x=1, y=5), Point(1, x=4, y=6), Point(2, x=0, y=7)))
        return triangle.area == 3.5
    def testTriangleArea3(self):
        triangle = (Triangle("test1", Point(0, x=34, y=26), Point(1, x=34, y=25), Point(2, x=35, y=25)))
        return triangle.area == 0.5

if __name__ == "__main__":
    unittest.main()
