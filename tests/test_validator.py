# tests/test_validator.py
import unittest
from dataDisk import Validator


class TestValidator(unittest.TestCase):
    def test_even_validator_pass(self):
        validator = Validator(lambda x: x % 2 == 0)
        result = validator.execute(4)
        self.assertEqual(result, 4)

    def test_even_validator_fail(self):
        validator = Validator(lambda x: x % 2 == 0)
        with self.assertRaises(ValueError):
            validator.execute(3)
