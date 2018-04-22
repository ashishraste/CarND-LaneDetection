import matplotlib.image as mimg
import matplotlib.pyplot as plt
import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip

import detection_util as du
import thresholds as th
from lane import *
import os
import argparse
import cv2

def detect_lanes_pipeline(actual_image):
  """
  Runs the lane-detection pipeline on a given image.
  :param actual_image:  Image in which the lanes have to be found.
  :return:  Image having marked lanes.
  """
  height,width,num_channels = actual_image.shape

  # Find lanes of yellow/white.
  color_filtered = du.color_filter(actual_image)

  # Get grayscale image.
  # gray = du.grayscale(color_filtered)
  gray = du.grayscale(actual_image)
  # plt.hist(gray.ravel(),256,[0,256])

  # Remove noise using Gaussian blur.
  gray_denoised = du.gaussian_blur(gray, th.GAUSSIAN_BLUR_KERNEL_SIZE)

  # Get image containing edges.
  edges = du.canny(gray_denoised, th.CANNY_LOW_THRESHOLD, th.CANNY_HIGH_THRESHOLD)

  # Clip the region containing the current lane.
  clipped_image = du.region_of_interest(edges,
                                        np.array([[(th.ROI_BOTTOM_LEFT_X,height), th.ROI_TOP_LEFT, th.ROI_TOP_RIGHT,
                                        (th.ROI_BOTTOM_RIGHT_X,height)]], dtype=np.int32))

  # Run a Hough transform on the image containing the edges to find lines.
  line_segments = du.hough_lines(clipped_image, th.HOUGH_RHO, th.HOUGH_THETA, th.HOUGH_NUM_VOTES_THRESHOLD,
                         th.HOUGH_MIN_LINE_LENGTH, th.HOUGH_MAX_LINE_GAP)

  # Draw Hough-lines on the actual image.
  lane_image = du.draw_lane(clipped_image, line_segments)

  if lane_image is not None:
    return du.weighted_img(lane_image, actual_image)
  else:
    return actual_image


def process_image(image):
  """
  Converts a video-frame to an image.
  :param image: Video frame.
  :return: Image with certain width and height parameters.
  """
  image_frame = cv2.resize(image, (th.IMAGE_WIDTH, th.IMAGE_HEIGHT))
  return detect_lanes_pipeline(image_frame)


if __name__ == '__main__':
  white_output = 'challengeOutput.mp4'
  clip1 = VideoFileClip('../test_videos/challenge.mp4')
  white_clip = clip1.fl_image(process_image)
  white_clip.write_videofile(white_output, audio=False)