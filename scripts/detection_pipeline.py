import matplotlib.image as mimg
import matplotlib.pyplot as plt
import numpy as np
import detection_util as du
import thresholds as th
import os
import argparse

def detect_lanes_pipeline(actual_image):
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
  hough_lines_image = du.hough_lines(clipped_image, th.HOUGH_RHO, th.HOUGH_THETA, th.HOUGH_NUM_VOTES_THRESHOLD,
                                     th.HOUGH_MIN_LINE_LENGTH, th.HOUGH_MAX_LINE_GAP)

  # Draw Hough-lines on the actual image.
  combined_image = du.weighted_img(hough_lines_image, actual_image)
  return combined_image



if __name__=='__main__':
  # Parse input and output directory paths.
  # parser = argparse.ArgumentParser()
  # parser.add_argument("input_dir", help="Input directory containing images.")
  # parser.add_argument("output_dir", help="Output directory where lane-images have to be saved.")
  # args = parser.parse_args()
  #
  # input_dir = args.input_dir
  # output_dir = args.output_dir

  input_dir = '../test_images'
  output_dir = '../test_images_output'

  image_files = os.listdir(input_dir)

  for file in image_files:
    # Load image.
    print(file)
    if file.endswith('.jpg'):
      image = mimg.imread(input_dir+'/'+file)
      # Run lane-detection-pipeline on the image.
      lanes_image = detect_lanes_pipeline(image)
      plt.imshow(lanes_image)
      plt.show()
      # du.write_img(lanes_image, output_dir+'/output_'+file)