import unittest

from billing import apply_discount


class DiscountTest(unittest.TestCase):
    def test_apply_discount(self) -> None:
        self.assertEqual(apply_discount(200, 10), 190)


if __name__ == "__main__":
    unittest.main()
