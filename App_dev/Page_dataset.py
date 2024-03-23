import os
import streamlit as st
import cv2
from PIL import Image
from streamlit_webrtc import webrtc_streamer
import uuid
import threading
from streamlit_extras.grid import grid
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container


def upload_images(selected_projects):
    # 创建一个用于保存图片的文件夹
    target_folder = os.path.join('projects', selected_projects)
    target_folder = os.path.join(target_folder, "datasets")
    target_folder = os.path.join(target_folder, "images")
    # 上传图片文件
    uploaded_files = st.file_uploader("上传图片", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    # st.write(uploaded_files)

    # 将上传的图片保存到指定文件夹中
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            # 获取上传文件的文件名
            filename = os.path.join(target_folder, uploaded_file.name)
            # 保存文件
            with open(filename, "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success(f"图片已成功保存到 {filename}。")


def upload_labels(selected_projects):
    # 创建一个用于保存标签的文件夹
    target_folder = os.path.join('projects', selected_projects)
    target_folder = os.path.join(target_folder, "datasets")
    target_folder = os.path.join(target_folder, "labels")

    # 上传标签文件
    uploaded_files = st.file_uploader("上传标签", type=["txt"], accept_multiple_files=True)
    # st.write(uploaded_files)

    # 将上传的标签保存到指定文件夹中
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            # 获取上传文件的文件名
            filename = os.path.join(target_folder, uploaded_file.name)
            # 保存文件
            with open(filename, "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success(f"标签已成功保存到 {filename}。")
def upload_classes(selected_projects):
    # 创建一个用于保存标签的文件夹
    target_folder = os.path.join('projects', selected_projects)
    target_folder = os.path.join(target_folder, "datasets")
    target_folder = os.path.join(target_folder, "labels")

    # 上传标签文件
    uploaded_files = st.file_uploader("上传class.txt", type=["txt"], accept_multiple_files=True)
    # st.write(uploaded_files)

    # 将上传的标签保存到指定文件夹中
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            # 获取上传文件的文件名
            filename = os.path.join(target_folder, uploaded_file.name)
            # 保存文件
            with open(filename, "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success(f"标签已成功保存到 {filename}。")


def get_all_projects():
    # 获取项目文件夹下的所有文件夹列表
    folder_list = [f.name for f in os.scandir('projects') if f.is_dir()]
    return folder_list


lock = threading.Lock()
img_container = {"img": None}


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    # img = frame
    with lock:
        img_container["img"] = img
    return frame


def count_lines_in_file(file_path):
    # 打开文件并逐行读取
    with open(file_path, 'r') as file:
        line_count = sum(1 for line in file)
    return line_count


def dataset_info(selected_projects):
    images_path = os.path.join('projects', selected_projects, 'datasets', 'images')
    if os.path.exists(images_path):
        images_files = os.listdir(images_path)
    else:
        os.makedirs(images_path)
        images_files = os.listdir(images_path)
    images_files = [file for file in images_files if os.path.isfile(os.path.join(images_path, file))]
    images_count = len(images_files)
    labels_path = os.path.join('projects', selected_projects, 'datasets', 'labels')
    if os.path.exists(labels_path):
        labels_files = os.listdir(labels_path)
    else:
        os.makedirs(labels_path)
        labels_files = os.listdir(labels_path)
    labels_files = [file for file in labels_files if os.path.isfile(os.path.join(labels_path, file))]
    labels_count = len(labels_files) - 1 if len(labels_files) - 1 >= 0 else 0
    try:
        classes_path = os.path.join('projects', selected_projects, 'datasets', 'labels', 'classes.txt')
        classes_count = count_lines_in_file(classes_path)
    except:
        classes_count = 0
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Images", value=images_count)
    col2.metric(label="Labels", value=labels_count)
    col3.metric(label="Class", value=classes_count)

    style_metric_cards()


def datasetPage(selected_projects):
    my_grid = grid( [4, 6],vertical_align="top")

    # Row 2:
    with my_grid.container():
        with stylable_container(
                key="green_button",
                css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """, ):
            dataset_info(selected_projects)

        with st.expander("导入图片", expanded=False):
            # 导入图片至目标项目
            upload_images(selected_projects)
        with st.expander("导入标签", expanded=False):
            # 导入标签至目标项目
            upload_labels(selected_projects)
        with st.expander("导入classes.txt", expanded=False):
            # 导入标签至目标项目
            upload_classes(selected_projects)

    with my_grid.container():
        with stylable_container(
                key="green_button",
                css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """, ):
            video_grid=grid([9, 1],vertical_align="top")
            with video_grid.container():
                webrtc_ctx = webrtc_streamer(key="demo", video_frame_callback=video_frame_callback)

            image_name = str(uuid.uuid4()) + ".png"
            save_path = os.path.join('projects', selected_projects, 'datasets', 'images', image_name)
            img = img_container["img"]
            if img is not None:
                pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            if 'count' not in st.session_state:
                st.session_state.count = 1
            with video_grid.container():
                st.metric(label="计数", value=st.session_state.count)

        with stylable_container(
                key="green_button",
                css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """, ):
            sub_grid = grid([2, 2], [8], [1], [1], [1], vertical_align="top")
            save_button=sub_grid.button("Save", use_container_width=True)
            reset_button=sub_grid.button("Reset", use_container_width=True)
            if save_button:
                pil_image.save(save_path)
                st.session_state.count += 1
                sub_grid.success(f"Saved to {save_path}  successfully")
                sub_grid.image(pil_image)
            if reset_button:
                st.session_state.count = 1
                st.experimental_rerun()
