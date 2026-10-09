import unittest

from billing import apply_discount


class HiddenDiscountTest(unittest.TestCase):
    def test_ten_percent(self) -> None:
        self.assertEqual(apply_discount(200, 10), 180)

    def test_zero(self) -> None:
        self.assertEqual(apply_discount(50, 0), 50)

    def test_quarter(self) -> None:
        self.assertEqual(apply_discount(80, 25), 60)


if __name__ == "__main__":
    unittest.main()
