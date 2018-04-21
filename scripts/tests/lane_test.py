from lane import *
import unittest
import math

class LineTest(unittest.TestCase):
  """ Unit test for Line class."""

  def test_line_segment_formation_with_ordered_endpoints(self):
    line1 = Line(2,3,10,15)
    self.assertEqual(2, line1.x1)
    self.assertEqual(3, line1.y1)
    self.assertEqual(10, line1.x2)
    self.assertEqual(15, line1.y2)
    self.assertEqual(1.5, line1.slope)
    self.assertEqual(0, line1.intercept)


  def test_line_segment_formation_with_unordered_endpoints(self):
    line1 = Line(50,22,10,30)
    self.assertEqual(10, line1.x1)
    self.assertEqual(30, line1.y1)
    self.assertEqual(50, line1.x2)
    self.assertEqual(22, line1.y2)


  def test_line_segment_with_infinity_slope(self):
    line = Line(30,20,30,120)
    self.assertEqual(math.inf, line.slope)


  def test_line_to_lane_side_association(self):
    # Positive slope.
    line1 = Line(10,20,40,100)
    self.assertEqual(Lane.RIGHT_LINE, line1.lane_side)

    # Infinite slope.
    line2 = Line(15,40,15,120)
    self.assertEqual(Lane.RIGHT_LINE, line2.lane_side)

    # Negative slope.
    line3 = Line(75,100,100,70)
    self.assertEqual(Lane.LEFT_LINE, line3.lane_side)


  def test_retrieve_line_segment_x_y_coordinates(self):
    line1 = Line(20,50,30,100)
    x_coords = line1.get_endpoint_x_coordinates()
    y_coords = line1.get_endpoint_y_coordinates()
    self.assertEqual(20, x_coords[0])
    self.assertEquals(30, x_coords[1])
    self.assertEqual(50, y_coords[0])
    self.assertEquals(100, y_coords[1])


if __name__ == '__main__':
  unittest.main()