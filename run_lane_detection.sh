#!/bin/bash

cd scripts
python detection_pipeline.py

echo 'Detection pipeline has successfully produced annotated videos in test_videos_output/ directory'
exit 0
