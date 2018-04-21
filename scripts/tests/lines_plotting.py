from lane import *
import detection_util as du
import thresholds as th
import detection_pipeline as dp
import matplotlib.pyplot as plt
import matplotlib.image as mimg

test_image = mimg.imread('../test_images/solidYellowCurve2.jpg')
left_line, right_line = dp.detect_lanes_pipeline(test_image)

