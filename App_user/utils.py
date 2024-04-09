#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
env: yolov8
requirements: ultralytics  ,streamlit_webrtc, streamlit
-------------------------------------------------
"""
import time
from ultralytics import YOLO
import streamlit as st
import cv2
from PIL import Image
import tempfile
from streamlit_webrtc import webrtc_streamer, RTCConfiguration, WebRtcMode
import av
import numpy as np
import threading
import subprocess
from ultralytics.nn.autobackend import check_class_names
from logic_check import logic_check
from output import output


def _display_detected_frames(conf, model, st_frame, image):

    # Resize the image to a standard size
    image = cv2.resize(image, (720, int(720 * (9 / 16))))

    # Predict the objects in the image using YOLOv8 model
    res = model.predict(image, conf=conf)

    # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True
                   )
    # return boxes


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

    classes_dir = model.names
    classes_list = list(classes_dir.values())

    return model, classes_list


def infer_uploaded_image(conf, model):
    """
    Execute inference for uploaded image
    :param conf: Confidence of YOLOv8 model
    :param model: An instance of the `YOLOv8` class containing the YOLOv8 model.
    :return: None
    """
    source_img = st.sidebar.file_uploader(
        label="Choose an image...",
        type=("jpg", "jpeg", "png", 'bmp', 'webp')
    )

    col1, col2 = st.columns(2)

    with col1:
        if source_img:
            uploaded_image = Image.open(source_img)
            # adding the uploaded image to the page with caption
            st.image(
                image=source_img,
                caption="Uploaded Image",
                use_column_width=True
            )

    if source_img:
        if st.button("Execution"):
            with st.spinner("Running..."):
                res = model.predict(uploaded_image,
                                    conf=conf)
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]

                with col2:
                    st.image(res_plotted,
                             caption="Detected Image",
                             use_column_width=True)
                    try:
                        with st.expander("Detection Results"):
                            for box in boxes:
                                st.write(box.xywh)
                    except Exception as ex:
                        # st.write("No image is uploaded yet!")
                        # st.write(ex)
                        print("error")


def infer_uploaded_video(conf, model):
    """
    Execute inference for uploaded video
    :param conf: Confidence of YOLOv8 model
    :param model: An instance of the `YOLOv8` class containing the YOLOv8 model.
    :return: None
    """
    source_video = st.sidebar.file_uploader(
        label="Choose a video..."
    )

    if source_video:
        st.video(source_video)

    if source_video:
        if st.button("Execution"):
            with st.spinner("Running..."):
                try:
                    tfile = tempfile.NamedTemporaryFile()
                    tfile.write(source_video.read())
                    vid_cap = cv2.VideoCapture(
                        tfile.name)
                    st_frame = st.empty()

                    while (vid_cap.isOpened()):
                        success, image = vid_cap.read()
                        if success:
                            _display_detected_frames(conf,
                                                     model,
                                                     st_frame,
                                                     image
                                                     )
                        else:
                            vid_cap.release()
                            break
                except Exception as e:
                    st.error(f"Error loading video: {e}")


def puttext(text, res_plotted, color):
    # 添加文字
    text = text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = color  # 白色
    # 获取文本的大小
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    text_position = ((res_plotted.shape[1] - text_size[0]) // 2, (res_plotted.shape[0] + text_size[1]) // 2)

    # 在图像上添加文字
    cv2.putText(res_plotted, text, text_position, font, font_scale, font_color, font_thickness)

    # 在图像边框涂成红色
    border_width = 10
    res_plotted[:border_width, :] = color
    res_plotted[-border_width:, :] = color
    res_plotted[:, :border_width] = color
    res_plotted[:, -border_width:] = color


def infer_uploaded_webcam_det(conf, model, target_list, logic, output_list, reaction_speed):
    """
    Execute inference for webcam.
    :param conf: Confidence of YOLOv8 model
    :param model: An instance of the `YOLOv8` class containing the YOLOv8 model.
    :return: None
    """

    # lock = threading.Lock()
    # frame_num = reaction_speed
    # zzl = [0] * frame_num

    def video_frame_callback(frame):
        # Resize the image to a standard size
        image = frame.to_ndarray(format="bgr24")
        # print("图像尺寸",image.shape)
        # image = cv2.resize(image, (640, 640))
        # image=np.fliplr(image)

        # Predict the objects in the image using YOLOv8 model
        res = model.predict(image, conf=conf, classes=target_list, vid_stride=5)
        boxes = res[0].boxes
        check = logic_check(logic, boxes)
        if check:
            result = "NOK"
            color = [0, 0, 255]
            output('Stop')
        else:
            result = "OK"
            color = [0, 255, 0]
            output('Reset')

        # Plot the detected objects on the video frame
        count = len(list(boxes.cls))
        res_plotted = res[0].plot()
        puttext(result, res_plotted, color)

        # with lock:
        #     if check ==True:
        #         zzl.append(1)
        #     elif check==False:
        #         zzl.append(0)
        return av.VideoFrame.from_ndarray(res_plotted, format="bgr24")

    stream = webrtc_streamer(
        key="example",
        video_frame_callback=video_frame_callback,

    )
    # while stream.state.playing:
    #     with lock:
    #         zzl = zzl[-1 * frame_num:]
    #         x = sum(zzl)
    #         time.sleep(0.001)
    #         if x > frame_num * 0.8:
    #             try:
    #                 for o in output_list:
    #                     output(o)
    #             except:
    #                 print('error, OUTPUT failed')
    #         else:
    #             output('Reset')
    #             continue
    st.write(str(target_list) + logic + str(output_list))
