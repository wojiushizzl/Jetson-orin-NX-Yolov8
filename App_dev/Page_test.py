
import os
import streamlit as st
import shutil
import ruamel.yaml
from  yolov8_train import train
from streamlit_extras.grid import grid
from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np
import av
from streamlit_webrtc import webrtc_streamer,RTCConfiguration,WebRtcMode

@st.cache_resource
def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.

    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model.
    """
    model = YOLO(model_path)
    st.write(model_path)

    return model

def infer_uploaded_webcam_det(conf, model):
    """
    Execute inference for webcam.
    :param conf: Confidence of YOLOv8 model
    :param model: An instance of the `YOLOv8` class containing the YOLOv8 model.
    :return: None
    """

    def video_frame_callback(frame):
        # Resize the image to a standard size
        image = frame.to_ndarray(format="bgr24")
        # print("图像尺寸",image.shape)
        # image = cv2.resize(image, (640, 640))
        # image=np.fliplr(image)

        # Predict the objects in the image using YOLOv8 model
        res = model.predict(image, conf=conf)
        boxes = res[0].boxes
        if len(list(boxes.cls)) > 0:
            result = "Detected"
            color=[0, 0, 255]
        else:
            result = "No detection"
            color = [0, 255, 0]
        # Plot the detected objects on the video frame
        count=len(list(boxes.cls))
        res_plotted = res[0].plot()

        # 添加文字
        text = result
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        font_color =color  # 白色
        # 获取文本的大小
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_position = ((res_plotted.shape[1] - text_size[0]) // 2, (res_plotted.shape[0] + text_size[1]) // 2)

        # 在图像上添加文字
        cv2.putText(res_plotted, text, text_position, font, font_scale, font_color, font_thickness)

        # 在图像边框涂成红色
        border_width = 10
        res_plotted[:border_width, :] =color
        res_plotted[-border_width:, :] =color
        res_plotted[:, :border_width] =color
        res_plotted[:, -border_width:] =color

        return av.VideoFrame.from_ndarray (res_plotted, format="bgr24")

    stream=webrtc_streamer(
        key="example",
        video_frame_callback=video_frame_callback,
        rtc_configuration={
            "iceServers":[{"urls":["stun:stun.1.google.com:19302"]}]
        }
    )

def get_last_updated_folder(folder_path):
    # 获取文件夹下的所有直接子文件夹
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    # 初始化最后更新的文件夹和最后更新时间
    last_updated_folder = None
    last_updated_time = 0

    # 遍历直接子文件夹
    for subfolder in subfolders:
        subfolder_path = os.path.join(folder_path, subfolder)
        # 获取文件夹的最后修改时间
        modified_time = os.path.getmtime(subfolder_path)
        # 比较最后修改时间，更新最后更新的文件夹和时间
        if modified_time > last_updated_time:
            last_updated_time = modified_time
            last_updated_folder = subfolder_path

    return last_updated_folder

def get_all_dir_list(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # last_train_path=get_last_updated_folder(train_path)
    dir_list=os.listdir(dir_path)
    # st.write(dir_list)
    return dir_list


def testpage(selected_projects):
    # 创建项目

    train_path=os.path.join('projects',selected_projects,'train')

    train_list=get_all_dir_list(train_path)
    train_type = None
    train_type = st.sidebar.selectbox(
            "Select Train",
            train_list
        )
    if train_type:
        model_path=os.path.join('projects',selected_projects,'train',train_type,'weights')
        model_list=get_all_dir_list(model_path)
        model_type=None
        model_type= st.sidebar.selectbox(
            "Select Model",
                model_list
        )

        confidence = float(st.sidebar.slider(
            "Select Model Confidence", 30, 100, 30)) / 100
        model_path = ""

        if model_type:
            model_path=os.path.join('projects',selected_projects,'train',train_type,'weights',model_type)
        else:
            st.error("Please Select Model in Sidebar")

        # load pretrained DL model
        try:
            model = load_model(model_path)
        except Exception as e:
            st.error(f"Unable to load model. Please check the specified path: {model_path}")

        infer_uploaded_webcam_det(confidence, model) # Detection task
