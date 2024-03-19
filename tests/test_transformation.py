import unittest
import numpy as np
from dataDisk import Transformation


class TestTransformation(unittest.TestCase):

    def test_impute_missing(self):
        data = [[1, np.nan], [3, 4]]
        expected = [[1, 4], [3, 4]]
        result = Transformation.impute_missing(data)
        np.testing.assert_allclose(result, expected, rtol=1e-5, atol=1e-8)

    def test_normalize(self):
        data = [[1, 4], [2, 3]]
        expected = [[0.24253563, 0.9701425 ],
                    [0.5547002 , 0.83205029]]
        result = Transformation.normalize(data)
        np.testing.assert_allclose(result, expected, rtol=1e-5, atol=1e-8)

    def test_onehot_encode(self):
        data = [['A', 'B'], ['A', 'C']]
        expected = [[1., 1., 0.], [1., 0., 1.]]
        result = Transformation.onehot_encode(data)
        np.testing.assert_allclose(result, expected, rtol=1e-5, atol=1e-8)

    def test_standardize(self):
        data = [[1, 2], [3, 4]]
        expected = [[-1, -1], [1, 1]]
        result = Transformation.standardize(data)
        np.testing.assert_allclose(result, expected, rtol=1e-5, atol=1e-8)


if __name__ == '__main__':
    unittest.main()