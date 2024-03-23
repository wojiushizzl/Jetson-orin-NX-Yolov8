#!/bin/bash

ls -l
source /home/zzl/archiconda3/etc/profile.d/conda.sh
conda activate yolov8
cd /home/zzl/Downloads/Jetson-orin-NX-env/streamlitapp/
streamlit run app.py
