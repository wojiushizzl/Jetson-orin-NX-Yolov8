
import os
import time
import datetime
import streamlit as st
import shutil
import ruamel.yaml
from  yolov8_train import train
from streamlit_extras.grid import grid
from streamlit_extras.stylable_container import stylable_container

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


def get_all_projects():
    # 获取项目文件夹下的所有文件夹列表
    folder_list = [f.name for f in os.scandir('projects') if f.is_dir()]
    return folder_list

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


def train_project(selected_projects):
    epochs=int(st.number_input('epochs',value=50))
    batch=int(st.number_input('batch',value=2))

    if st.button("训练项目"):
        train(selected_projects,epochs,batch)

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

def copy_file_in_place(src_file):
    try:
        # 获取文件的路径和文件名
        src_dir = os.path.dirname(src_file)
        src_filename = os.path.basename(src_file)

        # 构建目标文件的路径和文件名
        dest_file = os.path.join(src_dir, f"copy_of_{src_filename}")

        # 复制文件
        shutil.copy(src_file, dest_file)
        print(f"文件 {src_file} 已成功复制为 {dest_file}")
    except Exception as e:
        print(f"复制文件时出现错误: {e}")

def rename_and_copy(src_file, new_name, dest_folder):
    try:
        # 检查目标文件夹是否存在，如果不存在则创建
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        copy_file_in_place(src_file)
        new_file_path = os.path.join(dest_folder, new_name)


        # 重命名文件
        os.rename(src_file, new_file_path)


        print(f"文件 {src_file} 已成功重命名为 {new_name} 并复制至 {dest_folder}")
    except Exception as e:
        print(f"重命名和复制文件时出现错误: {e}")
        
def deploy(selected_projects):
    #move train/train*/weights/best.pt to App_user/weight/detection/
    train_path=os.path.join('projects',selected_projects,'train')
    if not os.path.exists(train_path):
        os.makedirs(train_path)
    last_train_path=get_last_updated_folder(train_path)
    st.write(last_train_path)
    if last_train_path is not None:
        best_path=os.path.join(last_train_path,'weights','best.pt')
        st.write(best_path)
        if st.button('一键部署'):
            current_time = datetime.datetime.now()
            new_name=selected_projects+str(current_time)+'.pt'
            rename_and_copy(best_path,new_name,'../App_user/weight/detection/')
            st.success('yep!')


def trainpage(selected_projects):
    # st.write(selected_projects)


    with st.expander("Update yaml file for training", expanded=True):
        # 更新yaml训练配置文件
        update_yaml(selected_projects)

    with st.expander("Start train", expanded=True):

        # 训练
        train_project(selected_projects)

    with st.expander("Deploy to User App", expanded=True):
        # 部署
        deploy(selected_projects)