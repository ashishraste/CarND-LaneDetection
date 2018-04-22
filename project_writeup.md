## **Finding Lane Lines on the Road**

---

**Finding Lane Lines on the Road**

The goals of the project are the following.
* Build an image-processing pipeline that finds lane lines on the road.

[//]: # (Image References)

[histogramOfIntensities]: ./test_images_output/histogramOfIntensities.png "Histogram"

---

### Reflection

### 1. Pipeline description

The image processing pipeline to find lane lines on the road in a given image consists of the following steps.

  1. The RGB image from a video-frame is converted to grayscale.
  Histogram of intensities could be plotted on the grayscale image to help tune
  the lower and upper bounds of intensities (for finding edges using Canny filter).
  Plot of one such histogram is shown below.

  ![alt text][histogramOfIntensities]

  2. Grayscale image is filtered using Gaussian blur (kernel-size = 3) to
  de-noise the image.

  3. Canny edge filtering is run on the de-noised image to find edges.

  4. The source image in grayscale form is masked with the region-of-interest
  (ROI) where we intend to find the current-lane. A bit of tuning is required to set the ROI polygon's vertices.

  5. Probabilistic Hough transform is performed on the masked image which gives
  us the set of line-segments found from the edges in the image.

  6. Linear regression is run on the line-segments, obtained from previous step,
  to find and draw the left and right lines of the current lane.


In order to draw a single line on the left and right lanes, following computations
are performed.

  - Line segments found from applying Hough transform are filtered based on their
  slopes in order to prune the ones resembling horizontal lines (slope close to 0).

  - Further, those line-segments are segregated into two sets of left and right
  line-segments, which (ideally) would belong to the left and right lines of the current-lane. This segregation is done based on the slope of the line-segments
  i.e. segments having negative-slope belong to the left-line and the ones having
  positive slope belong to the right-line.

  - Linear-regression (using `np.polyfit()`) is performed on these two sets of
  line-segments which gives us their respective line-equations.

  - (x,y) points are generated for these two lines using their line-equations,
  and they are extrapolated until the bottom of the image i.e. minimum-x = 0 for
  the left-line and maximum-y = height-of-the-image for the right-line.


### 2. Potential shortcomings with the current pipeline

Following shortcomings were observed with the pipeline described above.

1. Sensitivity to curved roads : Linear-regression performs poorly for finding
lane-lines which follow a curve of varying curvature.

2. Sensitivity to lane-color and lighting conditions : Above pipeline performs
poorly where the frames' lighting conditions switches rapidly (challenge video).

3. Tuning of parameters : Region of interest polygon where the pipeline looks for
lane lines vertices is not adaptive from a camera's perspective.

4. Slow refresh rate of lane-lines : As the pipeline is run on every single image
without any buffering of historical frames' lane-lines, the displayed lane-lines
where the lane-markers are discrete aren't continuous.  


### 3. Possible improvements to the detection pipeline

1. Buffering the pipeline's output (detected lane-lines) so as to output/display
a smooth lane.

2. Applying non-linear curve-fit on the line-segments given by Hough transform
and adjusting the length of detected lane-lines' accordingly.

3. Adaptive ROI selection, instead of current hardcoded vertices, to focus on an
image's region for finding lanes.
