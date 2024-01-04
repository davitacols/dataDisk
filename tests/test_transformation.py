# tests/test_transformation.py
import unittest
from dataDisk import Transformation


class TestTransformation(unittest.TestCase):
    def test_double_transformation(self):
        transformation = Transformation(lambda x: x * 2)
        result = transformation.execute(3)
        self.assertEqual(result, 6)

    def test_square_transformation(self):
        transformation = Transformation(lambda x: x ** 2)
        result = transformation.execute(4)
        self.assertEqual(result, 16)
