
import os
import streamlit as st
import shutil
import ruamel.yaml
from  yolov8_train import train
from streamlit_extras.grid import grid


def homepage(selected_projects):
    # 创建项目
    st.write('home')