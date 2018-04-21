from numpy import pi as PI

# Image resolution when converted from a video.
IMAGE_WIDTH = 960
IMAGE_HEIGHT = 540

# Color ranges in HSV space for yellow and white colors.
YELLOW_WHITE_COLOR_RANGE = ([0, 0, 210], [255, 255, 255])

# Gaussian blur.
GAUSSIAN_BLUR_KERNEL_SIZE = 3

# Canny edge detector's thresholds.
CANNY_LOW_THRESHOLD = 50
CANNY_HIGH_THRESHOLD = 170

# Region of interest vertices : 4-sided polygon.
ROI_BOTTOM_LEFT_X = 140
ROI_TOP_LEFT = (450,320)
ROI_TOP_RIGHT = (510,320)
ROI_BOTTOM_RIGHT_X = 880

# Hough transform parameters.
HOUGH_RHO = 1
HOUGH_THETA = PI/180
HOUGH_NUM_VOTES_THRESHOLD = 8
HOUGH_MIN_LINE_LENGTH = 10
HOUGH_MAX_LINE_GAP = 3