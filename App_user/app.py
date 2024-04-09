#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from PIL import Image
import streamlit as st
import config
from utils import *
from logic_check import LOGIC
from output import OUTPUT,output
import Jetson.GPIO as GPIO
import pyautogui
from streamlit_extras.grid import grid


# setting page layout
st.set_page_config(
    page_title="FAHAI",
    page_icon='../setup/logo.png',
    layout="wide",
    initial_sidebar_state="expanded",
)

RelayA = [21, 20, 26]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RelayA, GPIO.OUT, initial=GPIO.LOW)
# output('Stop')
if 'FULL' not in st.session_state :
    st.session_state.FULL=True
    pyautogui.press("f11")

def model_config():
    # model options
    # task_type = st.selectbox(
    #     "Select Task",
    #     config.TASK_TYPE_LIST
    # )
    task_type = 'Detection'
    model_type = None
    model_type = st.selectbox(
        "Select Model",
        config.MODEL_LIST[task_type]
    )

    confidence = float(st.slider(
        "Select Model Confidence", 30, 100, 30)) / 100

    model_path = ""

    if model_type:
        model_path = Path(config.MODEL_DIR[task_type], str(model_type))
    else:
        st.error("Please Select Model in Sidebar")

    # load pretrained DL model
    try:
        model, classes_list = load_model(model_path)

    except Exception as e:
        st.error(f"Unable to load model. Please check the specified path: {model_path}")
    return task_type, model, confidence, classes_list


def source_switch():
    # image/video options
    source_selectbox = st.selectbox(
        "Select Source",
        config.SOURCES_LIST,
        index=2
    )
    return source_selectbox


def target_select(classes_list):
    '''
      find the classes from the project , output classes selected list 
      target_list:list[int]
    '''
    target_list = st.multiselect("Target", classes_list, default=[classes_list[0]])
    target_list_index = []
    for t in target_list:
        target_list_index.append(classes_list.index(t))
    # st.write(target_list_index)
    return target_list_index


def logic_select():
    ### select the logic  ###
    logic = st.selectbox("Logic", LOGIC, index=0)
    return logic


def output_select():
    ### select the output ###
    output_list = st.multiselect("Output", OUTPUT[:-1], default=OUTPUT[2])
    reaction_speed = int(st.slider(
        "Select Reaction Speed", 10, 100, 30))

    return output_list, reaction_speed

def buttons():
    button_grid=grid([2,2,2],vertical_align='top')
    reset_button = button_grid.button('OPEN')
    stop_button =button_grid.button('STOP')
    fullscreen_button=button_grid.button('FULL')
    if reset_button:
        output('Reset')
        # st.rerun()
        # pyautogui.press('f5')
    if stop_button:
        output('Stop')
    if fullscreen_button:
        pyautogui.press('f11')
        st.session_state.FULL= not st.session_state.FULL


# sidebar
with st.sidebar:
    with st.expander("Operate", expanded=True):
        buttons()
    with st.expander("Model Config", expanded=True):
        task_type, model, confidence, classes_list = model_config()
    with st.expander("Video&Image Switch", expanded=False):
        source_selectbox = source_switch()
    with st.expander("Target Select", expanded=False):
        target_list = target_select(classes_list)
    with st.expander("Logic Select", expanded=False):
        logic = logic_select()
    with st.expander("Output Select", expanded=True):
        output_list, reaction_speed = output_select()

# st.write(classes_list)
source_img = None

if source_selectbox == config.SOURCES_LIST[0]:  # Image
    infer_uploaded_image(confidence, model)
elif source_selectbox == config.SOURCES_LIST[1]:  # Video
    infer_uploaded_video(confidence, model)
elif source_selectbox == config.SOURCES_LIST[2]:  # Webcam
    if task_type == config.TASK_TYPE_LIST[0]:
        infer_uploaded_webcam_det(confidence, model, target_list, logic, output_list, reaction_speed,
                                  )  # Detection task


else:
    st.error("Currently only 'Image' and 'Video' source are implemented")
