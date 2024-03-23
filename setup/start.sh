#!/bin/bash

#ls -l
source /home/zzl/archiconda3/etc/profile.d/conda.sh
conda activate yolov8
cd /home/zzl/Downloads/Jetson-orin-NX-Yolov8/App_user
streamlit run app.py
