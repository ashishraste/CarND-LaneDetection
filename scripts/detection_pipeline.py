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
  image_frame = cv2.resize(image, (th.IMAGE_WIDTH, th.IMAGE_HEIGHT))
  return detect_lanes_pipeline(image_frame)


if __name__ == '__main__':
  white_output = 'challengeOutput.mp4'
  clip1 = VideoFileClip('../test_videos/challenge.mp4')
  white_clip = clip1.fl_image(process_image)
  white_clip.write_videofile(white_output, audio=False)

# if __name__=='__main__':
#   # Parse input and output directory paths.
#   # parser = argparse.ArgumentParser()
#   # parser.add_argument("input_dir", help="Input directory containing images.")
#   # parser.add_argument("output_dir", help="Output directory where lane-images have to be saved.")
#   # args = parser.parse_args()
#   #
#   # input_dir = args.input_dir
#   # output_dir = args.output_dir
#
#   input_dir = '../test_images'
#   output_dir = '../test_images_output'
#
#   image_files = os.listdir(input_dir)
#
#   for file in image_files:
#     # Load image.
#     print(file)
#     if file.endswith('.jpg'):
#       image = mimg.imread(input_dir+'/'+file)
#
#       # Run lane-detection-pipeline on the image.
#       lanes_image = detect_lanes_pipeline(image)
#       plt.imshow(lanes_image)
#       plt.show()
#       du.write_img(lanes_image, output_dir+'/output_'+file)

# if __name__=='__main__':
#   test_image = mimg.imread('../test_images/solidYellowCurve.jpg')
#   lanes_image = detect_lanes_pipeline(test_image)
#   plt.imshow(lanes_image)
#   plt.show()