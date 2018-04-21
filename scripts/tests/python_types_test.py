import unittest
from lane import *
import math

class TypesTest(unittest.TestCase):
  """
  Unit test for Python types and built-in functions.
  """

  def test_something(self):
    lines = []
    line1 = np.array([[75,100,100,70]], dtype=int)
    line2 = np.array([[15,40,15,120]], dtype=int)
    lines.append(line1)
    lines.append(line2)
    self.assertIsNotNone(lines)

    line_segments = list(map(lambda line: Line(*line[0]),lines))

    line_seg1 = line_segments[0]
    line_seg2 = line_segments[1]
    self.assertEqual(Lane.LEFT_LINE, line_seg1.lane_side)
    self.assertEqual(Lane.RIGHT_LINE, line_seg2.lane_side)
    self.assertEqual(math.inf, line_seg2.slope)


if __name__ == '__main__':
  unittest.main()
