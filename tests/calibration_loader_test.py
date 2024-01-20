import unittest
from unittest.mock import patch
from calibration_loader_test import load_calibration


class CalibrationLoaderTest(unittest.TestCase):
    @patch("builtins.open")
    def test_load_calibration(self, mock_open):
        # Define the contents of the calibration.txt file
        mock_open.return_value.__enter__.return_value.readlines.return_value = [
            "red_lower: 0.1, 0.2, 0.3\n",
            "red_upper: 0.4, 0.5, 0.6\n",
            "green_lower: 0.7, 0.8, 0.9\n",
            "green_upper: 1.0, 1.1, 1.2\n",
            "blue_lower: 1.3, 1.4, 1.5\n",
            "blue_upper: 1.6, 1.7, 1.8\n",
        ]

        # Call the function
        (
            red_lower,
            red_upper,
            green_lower,
            green_upper,
            blue_lower,
            blue_upper,
        ) = load_calibration()

        # Assert the expected values
        self.assertEqual(red_lower, [0.1, 0.2, 0.3])
        self.assertEqual(red_upper, [0.4, 0.5, 0.6])
        self.assertEqual(green_lower, [0.7, 0.8, 0.9])
        self.assertEqual(green_upper, [1.0, 1.1, 1.2])
        self.assertEqual(blue_lower, [1.3, 1.4, 1.5])
        self.assertEqual(blue_upper, [1.6, 1.7, 1.8])


if __name__ == "__main__":
    unittest.main()
