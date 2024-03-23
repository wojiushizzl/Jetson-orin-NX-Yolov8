#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
env: yolov8
requirements: ultralytics
-------------------------------------------------
"""
from pathlib import Path
import sys
import os


# Get the absolute path of the current file
file_path = Path(__file__).resolve()

# Get the parent directory of the current file
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the current working directory
ROOT = root_path.relative_to(Path.cwd())


# Source
SOURCES_LIST = ["Image", "Video", "Webcam"]

TASK_TYPE_LIST = ["Detection","Classification"]

MODEL_DIR={
    "Detection":ROOT / 'weight' / 'detection',
    "Classification":ROOT / 'weight' / 'classification'
}

if not os.path.exists(str(MODEL_DIR[TASK_TYPE_LIST[0]])):
    os.makedirs(str(MODEL_DIR[TASK_TYPE_LIST[0]]))
if not os.path.exists(str(MODEL_DIR[TASK_TYPE_LIST[1]])):
    os.makedirs(str(MODEL_DIR[TASK_TYPE_LIST[1]]))
DETECTION_MODEL_LIST = os.listdir(str(MODEL_DIR[TASK_TYPE_LIST[0]]))
CLS_MODEL_LIST = os.listdir(str(MODEL_DIR[TASK_TYPE_LIST[1]]))


MODEL_LIST={
    "Detection":DETECTION_MODEL_LIST,
    "Classification":CLS_MODEL_LIST
}

