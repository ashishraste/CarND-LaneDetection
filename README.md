#### Lane Detection

---

This repository contains the Lane Detection project (Project 1) of [Udacity's
Self Driving Car Nanodegree](https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013).

---

#### Directory layout

1. lane_lines_detection.ipynb : Ipython notebook containing the project's
lane-lines-detection pipeline.

2. project_writeup.md : Writeup on the detection pipeline used in the project,
including its shortcomings and potential improvements.

3. test_images : Sample images to test the detection pipeline.

4. test_images_output : Annotated output given by the detection-pipeline, after
having run on the test-images.

5. test_videos : Sample videos to test the detection pipeline.

6. test_videos_output : Contains annotated video outputs, having detected lane,
of input videos residing in the test_videos/ directory.

7. scripts : Sources containing the detection pipeline and some of their unit-tests.

8. run_lane_detection.sh : Shell script to run the detection pipeline on the two
videos inside test_videos/ directory.

---

#### Running the lane-detection pipeline

Note: Below instructions are only supported for Unix shells.

From the parent directory run the following.

`sh run_lane_detection.sh`

Output videos are saved inside test_videos_output/ directory.

---
