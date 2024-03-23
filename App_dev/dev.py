#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import os
import streamlit as st
import hydralit_components as hc
import datetime
from Page_home import homepage
from Page_dataset import datasetPage
from Page_train import trainpage
from Page_test import testpage
from streamlit_option_menu import option_menu
import shutil
import ruamel.yaml

# make it look nice from the start
st.set_page_config(
    page_title="FAHAI_dev",
    page_icon='/home/zzl/Desktop/logo.png',
    layout='wide',
    # initial_sidebar_state='collapsed',
)
def get_all_projects():
    # 获取项目文件夹下的所有文件夹列表
    folder_list = [f.name for f in os.scandir('projects') if f.is_dir()]
    return folder_list

yaml = ruamel.yaml.YAML()
def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
    except FileExistsError:
        st.error(f'文件夹 "{folder_name}" 已经存在。')


def create_yaml(project_name):
    file_name=project_name+'/train.yaml'
    # 复制文件
    shutil.copyfile("train.yaml", file_name)

    # 读取复制的文件并更改其中一行代码
    with open(file_name, "r", encoding="utf-8") as file:
        lines = yaml.load(file)

    path=os.path.join(project_name, 'datasets')
    if "path" in lines:
        lines["path"] =path

    # 将更改后的内容写回文件
    with open(file_name, "w", encoding="utf-8") as file:
        yaml.dump(lines, file)

def get_all_classes(project_name):
    classes_txt_path=os.path.join('projects',project_name,'datasets','labels','classes.txt')
    result_dict = {}
    if os.path.exists(classes_txt_path):
        with open(classes_txt_path, 'r') as file:
            lines = file.readlines()
            for i,line in enumerate(lines):
                result_dict[i] = line.strip()
        return result_dict
    else:
        return False


def update_yaml(project_name):
    if st.button("更新训练配置文件"):
        file_name=os.path.join('projects',project_name,'train.yaml')

        # 读取复制的文件并更改其中一行代码
        with open(file_name, "r", encoding="utf-8") as file:
            lines = yaml.load(file)

        classes=get_all_classes(project_name)
        if classes :
            if "names" in lines:
                lines["names"] =classes

            # 将更改后的内容写回文件
            with open(file_name, "w", encoding="utf-8") as file:
                yaml.dump(lines, file)
            st.success('yaml file updated')
        else:
            st.error('分类文件不存在，请先上传classes.txt')

def create_project():
    # 创建项目
    project_name = st.text_input('输入项目名称：')

    message_container = st.empty()
    folder_name = os.path.join('projects', project_name)
    if st.button('创建项目'):
        if project_name:
            try:
                create_folder(folder_name)
                subfolder_path = os.path.join(folder_name, 'datasets')
                create_folder(subfolder_path)
                imagefolder_path = os.path.join(subfolder_path, 'images')
                create_folder(imagefolder_path)
                labelfolder_path = os.path.join(subfolder_path, 'labels')
                create_folder(labelfolder_path)
                create_yaml(folder_name)
                st.rerun()
                message_container.success(f'项目 "{project_name}" 创建成功！')

            except FileExistsError:
                message_container.error(f'项目 "{project_name}" 已经存在。')
        else:
            message_container.warning('请输入项目称。')

def delete_project(selected_projects):
    #删除项目
    if st.button('删除项目'):
        if selected_projects:
            try:
                selected_projects = os.path.join('projects', selected_projects)
                # 删除文件夹及其内容
                shutil.rmtree(selected_projects)
                st.success(f'项目 "{selected_projects}" 删除成功！')
                st.rerun()

            except FileExistsError:
                st.error(f'项目 "{selected_projects}" 不存在。')
        else:
            st.warning('请选择项目。')


# 选择项目

def sidebar_setting():
    projects_list = get_all_projects()
    # 1. as sidebar menu
    with st.sidebar:
        selected_project = option_menu(
            "Select Projects",
            options=projects_list,
            # icons=['house'],
            menu_icon="cast",
            default_index=0
        )
    with st.sidebar:
        with st.expander("Create Project", expanded=False):
            # 创建项目
            create_project()
        with st.expander("Delete Project", expanded=False):
            # 删除项目
            st.write(selected_project)
            delete_project(selected_project)
    menu_data = [
        {'icon': "far fa-copy", 'label': "Datasets"},
        {'icon': "far fa-chart-bar", 'label': "Train"},  # no tooltip message
    ]

    over_theme = {'txc_inactive': 'white', 'menu_background': '#000080'}
    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        use_animation=True,
        home_name='Home',
        login_name='Test',
        hide_streamlit_markers=True,  # will show the st hamburger as well as the navbar now!
        sticky_nav=True,  # at the top or not
        sticky_mode='pinned',  # jumpy or not-jumpy, but sticky or pinned
    )
    return menu_id,selected_project
menu_id,selected_project=sidebar_setting()
# get the id of the menu item clicked
# st.info(f"{menu_id}")




if menu_id == 'Home':
    homepage(selected_project)

if menu_id == 'Datasets':
    datasetPage(selected_project)

if menu_id == 'Train':
    trainpage(selected_project)

if menu_id == 'Test':
    testpage(selected_project)