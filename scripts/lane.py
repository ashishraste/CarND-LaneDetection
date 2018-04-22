import numpy as np
import thresholds as th
import math

class Lane(object):
  """ Encapsulation of a lane's properties."""

  # Static fields.
  LEFT_LINE = 'left'
  RIGHT_LINE = 'right'
  APPROX_HORIZONTAL_LINE_SLOPE = 0.4


class Line(object):
  """ Represents a 2D line-segment in Euclidean coordinate system."""

  def __init__(self, x1, y1, x2, y2):
    # Ordering the endpoints from left to right as in a traditional xy coordinate system viewpoint.
    if x1 > x2:
      (x1, y1), (x2, y2) = (x2, y2), (x1, y1)
    self.x1, self.y1 = x1, y1
    self.x2, self.y2 = x2, y2
    self.slope = self.calculate_slope()
    self.intercept = self.calculate_intercept()
    # Tells which part of the lane-side this this line-segment belongs to, based on its slope.
    self.lane_side = self.filter_lane_line_side()

  def __repr__(self):
    return "x1={} y1={} x2={} y2={} slope={} y-intercept={}".format(self.x1, self.y1, self.x2, self.y2, self.slope,
                                                                    self.intercept)

  def calculate_slope(self):
    """ Calculates slope of a line."""
    if abs(self.x2 - self.x1) == 0:
      return math.inf
    return (self.y2 - self.y1) / (self.x2 - self.x1)

  def calculate_intercept(self):
    """ Calculates the y-intercept of a line."""
    return self.y1 - self.slope * self.x1

  def filter_lane_line_side(self):
    if self.slope < 0.0:
      return Lane.LEFT_LINE
    else:
      return Lane.RIGHT_LINE

  def get_endpoint_x_coordinates(self):
    return [self.x1, self.x2]

  def get_endpoint_y_coordinates(self):
    return [self.y1, self.y2]

  @property
  def is_candidate(self):
    """
    Checks whether a line-segment is a good candidate for a given lane-line (left or right).
    If the line-segment's slope is closer to a horizontal line's, then it is ignored.
    :return: Boolean value of a line-segment being a candidate.
    """
    if abs(self.slope) < Lane.APPROX_HORIZONTAL_LINE_SLOPE:
      return False
    return True