import unittest
import cv2
from tri_colour_detection import detect_colors


class TestColorDetection(unittest.TestCase):
    def setUp(self):
        self.webcam = cv2.VideoCapture(0)

    def tearDown(self):
        self.webcam.release()
        cv2.destroyAllWindows()

    def test_detect_colors(self):
        colors = detect_colors(self.webcam)
        self.assertIsInstance(colors, dict)
        self.assertIn("red", colors)
        self.assertIn("green", colors)
        self.assertIn("blue", colors)
        self.assertIsInstance(colors["red"], list)
        self.assertIsInstance(colors["green"], list)
        self.assertIsInstance(colors["blue"], list)
        self.assertGreater(len(colors["red"]), 0)
        self.assertGreater(len(colors["green"]), 0)
        self.assertGreater(len(colors["blue"]), 0)


if __name__ == "__main__":
    unittest.main()
