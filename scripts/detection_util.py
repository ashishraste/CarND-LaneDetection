import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import thresholds as th
from lane import *

def grayscale(img):
  """Applies the Grayscale transform
  This will return an image with only one color channel"""
  # Using BGR2GRAY to read an image with cv2.imread()
  return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def color_filter(img):
  """Filters the image for a given color space.
  Here we look for yellow and white colors which represent the lane lines.
  """
  lower, upper = th.YELLOW_WHITE_COLOR_RANGE
  lower = np.array(lower, dtype=np.uint8)
  upper = np.array(upper, dtype=np.uint8)

  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV);
  yellow_white_mask = cv2.inRange(hsv, lower, upper)
  return yellow_white_mask


def canny(img, low_threshold, high_threshold):
  """Applies the Canny transform"""
  return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):
  """Applies a Gaussian Noise kernel"""
  return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices):
  """
  Applies an image mask.

  Only keeps the region of the image defined by the polygon
  formed from `vertices`. The rest of the image is set to black.
  """
  # defining a blank mask to start with
  mask = np.zeros_like(img)

  # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
  if len(img.shape) > 2:
    channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,) * channel_count
  else:
    ignore_mask_color = 255

  # filling pixels inside the polygon defined by "vertices" with the fill color
  cv2.fillPoly(mask, vertices, ignore_mask_color)
  # plt.imshow(mask)
  # plt.show()

  # returning the image only where mask pixels are nonzero
  masked_image = cv2.bitwise_and(img, mask)
  return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
  """
  NOTE: this is the function you might want to use as a starting point once you want to
  average/extrapolate the line segments you detect to map out the full
  extent of the lane (going from the result shown in raw-lines-example.mp4
  to that shown in P1_example.mp4).

  Think about things like separating line segments by their
  slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
  line vs. the right line.  Then, you can average the position of each of
  the lines and extrapolate to the top and bottom of the lane.

  This function draws `lines` with `color` and `thickness`.
  Lines are drawn on the image inplace (mutates the image).
  If you want to make the lines semi-transparent, think about combining
  this function with the weighted_img() function below
  """
  for line in lines:
    for x1, y1, x2, y2 in line:
      cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def draw_lane_lines(img, left_line_pts, right_line_pts, color=[255,0,0], thickness=5):
  """
  Draws left and right lane lines on an image.
  :param img: Source image on which the lane-lines have to be drawn.
  :param left_line_pts: Points belonging to the left line of the lane.
  :param right_line_pts: Points belonging to the right line of the lane.
  :param color: RGB color of the line to be drawn.
  :param thickness: Thickness of the line to be drawn.
  """
  # Draw left line of the lane.
  cv2.line(img, left_line_pts[0], left_line_pts[-1], color, thickness)
  # Draw right line of the lane.
  cv2.line(img, right_line_pts[0], right_line_pts[-1], color, thickness)

def draw_lane(img, line_segments):
  """
  :param line_segments:  Line segments obtained using Hough transform.
  :return:  Image containing marked lanes.
  """
  # Line fit on obtained hough-lines.
  if line_segments is not None:
    left_line_segments = [segment for segment in line_segments if segment.lane_side == Lane.LEFT_LINE]
    right_line_segments = [segment for segment in line_segments if segment.lane_side == Lane.RIGHT_LINE]
    left_line_x, left_line_y = get_x_y_coordinates_as_list(left_line_segments)
    right_line_x, right_line_y = get_x_y_coordinates_as_list(right_line_segments)

    if len(left_line_x) == 0 or len(left_line_y) == 0 or len(right_line_x) == 0 or len(right_line_y) == 0:
      return None

    left_coeffs = np.polyfit(left_line_x, left_line_y, 1)
    right_coeffs = np.polyfit(right_line_x, right_line_y, 1)

    left_line = np.poly1d(left_coeffs)
    right_line = np.poly1d(right_coeffs)

    # Generate left-line and right-line's points.
    # Note: Minimum x-coordinate that can be observed is 0.
    x_left = np.linspace(0, max(left_line_x), 10).astype(int)
    y_left = left_line(x_left).astype(int)
    left_line_pts = list(zip(x_left, y_left))
    # Note: Maximum x-coordinate that can be observed is image's width.
    x_right = np.linspace(min(right_line_x), img.shape[1], 10).astype(int)
    y_right = right_line(x_right).astype(int)
    right_line_pts = list(zip(x_right, y_right))

    lines_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lane_lines(lines_img, left_line_pts, right_line_pts)
    return lines_img


def get_x_y_coordinates_as_list(line_segments):
  """
  Returns x-coordinates and y-coordinates as separate lists.
  :param line_segments: Line segments containing x and y coordinates.
  """
  line_x_coords = []
  line_y_coords = []

  for line_seg in line_segments:
    line_x_coords += line_seg.get_endpoint_x_coordinates()
    line_y_coords += line_seg.get_endpoint_y_coordinates()

  return line_x_coords,line_y_coords


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
  """
  `img` should be the output of a Canny transform.

  Returns an image with hough lines drawn.
  """
  lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
  filtered_lines = list(filter(lambda l: l.is_candidate, map(lambda line: Line(*line[0]), lines)))
  if filtered_lines is not None:
    return filtered_lines
  else:
    return None


# Python 3 has support for cool math symbols.
def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
  """
  `img` is the output of the hough_lines(), An image with lines drawn on it.
  Should be a blank image (all black) with lines drawn on it.

  `initial_img` should be the image before any processing.

  The result image is computed as follows:

  initial_img * α + img * β + γ
  NOTE: initial_img and img must be the same shape!
  """
  return cv2.addWeighted(initial_img, α, img, β, γ)


def write_img(img, path=os.getcwd()+'/processed_lane.jpg'):
  """

  :param img: Source image to be saved.
  :param path: File path of the image to be saved.
  :return: None.

  NOTE: The color channels are flipped i.e. RGB -> BGR while writing an image to a file.
  """
  cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY,95])