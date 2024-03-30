import os
import time
import datetime
import streamlit as st
import shutil
import ruamel.yaml
from yolov8_train import train
from streamlit_extras.grid import grid
from streamlit_extras.stylable_container import stylable_container
import hydralit_components as hc
import pandas as pd

yaml = ruamel.yaml.YAML()


def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
    except FileExistsError:
        st.error(f'文件夹 "{folder_name}" 已经存在。')


def create_yaml(project_name):
    file_name = project_name + '/train.yaml'
    # 复制文件
    shutil.copyfile("train.yaml", file_name)

    # 读取复制的文件并更改其中一行代码
    with open(file_name, "r", encoding="utf-8") as file:
        lines = yaml.load(file)

    path = os.path.join(project_name, 'datasets')
    if "path" in lines:
        lines["path"] = path

    # 将更改后的内容写回文件
    with open(file_name, "w", encoding="utf-8") as file:
        yaml.dump(lines, file)


def get_all_classes(project_name):
    classes_txt_path = os.path.join('projects', project_name, 'datasets', 'labels', 'classes.txt')
    result_dict = {}
    if os.path.exists(classes_txt_path):
        with open(classes_txt_path, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                result_dict[i] = line.strip()
        return result_dict
    else:
        return False


def update_yaml(project_name):
    if st.button("更新训练配置文件"):
        file_name = os.path.join('projects', project_name, 'train.yaml')

        # 读取复制的文件并更改其中一行代码
        with open(file_name, "r", encoding="utf-8") as file:
            lines = yaml.load(file)

        classes = get_all_classes(project_name)
        if classes:
            if "names" in lines:
                lines["names"] = classes

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
    # 删除项目
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
    train_grid = grid([2, 2,2], [1], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], vertical_align="bottom")
    name=train_grid.text_input('Comments',f"train_for_{selected_projects}")

    epochs = int(train_grid.number_input('epochs', value=50,
                                         help="训练历元总数。每个历元代表对整个数据集进行一次完整的训练。调整该值会影响训练时间和模型性能。"))
    batch = int(train_grid.number_input('batch', value=2,
                                        help="训练的批量大小，表示在更新模型内部参数之前要处理多少张图像。自动批处理 (batch=-1)会根据 GPU 内存可用性动态调整批处理大小。"))
    train_grid.write("高级设置")
    exist_ok = train_grid.toggle("exist_ok",
                                 help="如果为 True，则允许覆盖现有的项目/名称目录。这对迭代实验非常有用，无需手动清除之前的输出。")
    single_cls = train_grid.toggle("single_cls",
                                   help="在训练过程中将多类数据集中的所有类别视为单一类别。适用于二元分类任务，或侧重于对象的存在而非分类。")
    patience = int(train_grid.number_input('patience', min_value=10, max_value=epochs, value=20,
                                           help="在验证指标没有改善的情况下，提前停止训练所需的历元数。当性能趋于平稳时停止训练，有助于防止过度拟合。"))
    imgsz = int(train_grid.number_input('imgsz', min_value=480, value=640,
                                        help="用于训练的目标图像尺寸。所有图像在输入模型前都会被调整到这一尺寸。影响模型精度和计算复杂度。"))
    degrees = int(train_grid.slider('degrees', min_value=-180, max_value=180, value=20,
                                    help="float -180 - +180  在指定的度数范围内随机旋转图像，提高模型识别不同方向物体的能力。"))
    translate = int(train_grid.slider('translate', min_value=0.0, max_value=1.0, value=0.1, step=0.1,
                                      help="float  0.0 - 1.0	以图像大小的一小部分水平和垂直平移图像，帮助学习检测部分可见的物体。"))
    scale = int(train_grid.slider('scale', min_value=0.0, max_value=1.0, value=0.5, step=0.1,
                                  help=" float 0.0 - 1.0  通过增益因子缩放图像，模拟物体与摄像机的不同距离。"))
    flipud = int(train_grid.slider('flipud', min_value=0.0, max_value=1.0, value=0.0, step=0.1,
                                   help="float  0.0 - 1.0 以指定的概率将图像翻转过来，在不影响物体特征的情况下增加数据的可变性。"))
    fliplr = int(train_grid.slider('fliplr', min_value=0.0, max_value=1.0, value=0.0, step=0.1,
                                   help="float 0.0 - 1.0  以指定的概率将图像从左到右翻转，这对学习对称物体和增加数据集多样性非常有用。"))
    erasing = int(train_grid.slider('erasing', min_value=0.0, max_value=1.0, value=0.4, step=0.1,
                                    help="float 0.0 - 1.0  在分类训练过程中随机擦除部分图像，鼓励模型将识别重点放在不明显的特征上。"))
    mosaic = int(train_grid.slider('mosaic', min_value=0.0, max_value=1.0, value=1.0, step=0.1,
                                   help=" float  0.0 - 1.0将四幅训练图像合成一幅，模拟不同的场景构成和物体互动。对复杂场景的理解非常有效。"))
    mixup = int(train_grid.slider('mixup', min_value=0.0, max_value=1.0, value=0.0, step=0.1,
                                  help="float 0.0 - 1.0  混合两幅图像及其标签，创建合成图像。通过引入标签噪声和视觉变化，增强模型的泛化能力。"))
    copy_paste = int(train_grid.slider('copy_paste', min_value=0.0, max_value=1.0, value=0.0, step=0.1,
                                       help="float 0.0 - 1.0  从一幅图像中复制物体并粘贴到另一幅图像上，用于增加物体实例和学习物体遮挡。"))

    if st.button("训练项目"):
        train(
            name=name,
            project_name=selected_projects,
            epochs=epochs,
            batch=batch,
            exist_ok=exist_ok,
            single_cls=single_cls,
            patience=patience,
            imgsz=imgsz,
            degrees=degrees,
            translate=translate,
            scale=scale,
            flipud=flipud,
            fliplr=fliplr,
            erasing=erasing,
            mosaic=mosaic,
            mixup=mixup,
            copy_paste=copy_paste)


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
    # move train/train*/weights/best.pt to App_user/weight/detection/
    train_path = os.path.join('projects', selected_projects, 'train')
    if not os.path.exists(train_path):
        os.makedirs(train_path)
    last_train_path = get_last_updated_folder(train_path)

    if last_train_path is not None:
        st.write(f"last_train_path :{last_train_path}")
        best_path = os.path.join(last_train_path, 'weights', 'best.pt')
        st.write(f"last train weights file path :{best_path}")
        if st.button('一键部署'):
            current_time = datetime.datetime.now()
            new_name = selected_projects + str(current_time) + '.pt'
            rename_and_copy(best_path, new_name, '../App_user/weight/detection/')
            st.success('Deploy to User App SUCCESS!')
    else:
        st.warning("No train result")

# 用于遍历文件夹中的所有image文件
def list_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):  # 筛选出图片文件
                file_list.append(os.path.join(root, file))
    return file_list


def train_result_show(selected_projects):
    train_path = os.path.join('projects', selected_projects, 'train')
    if not os.path.exists(train_path):
        os.makedirs(train_path)
    last_train_path = get_last_updated_folder(train_path)
    if last_train_path is not None:
        st.write(f"last_train_path :{last_train_path}")
        try:
            image_list = list_files(last_train_path)
            if image_list is not None:
                for img in image_list:
                    st.image(img, caption=os.path.basename(img), use_column_width=True)
        except:
            st.warning("No train reslut")
    else:
        st.warning("No train reslut")


def train_progress(selected_projects):
    train_path = os.path.join('projects', selected_projects, 'train')
    if not os.path.exists(train_path):
        os.makedirs(train_path)
    last_train_path = get_last_updated_folder(train_path)
    if last_train_path is not None:
        st.write(f"last_train_path :{last_train_path}")
        try:
            results_csv=os.path.join(last_train_path,'results.csv')
            args_yaml_path=os.path.join(last_train_path,'args.yaml')
            # st.write(results_csv)
            # st.write(args_yaml_path)
            with open(args_yaml_path, 'r') as stream:
                yaml_data = yaml.load(stream)

            # 获取你想要的值，假设键为key_name
            value = yaml_data['epochs']
            # st.write(value)
            # 读取CSV文件
            df = pd.read_csv(results_csv)
            st.dataframe(df)
            # 获取名为"epoch"的列的最大值
            max_epoch =  df.shape[0]

            override_theme = {'content_color': 'white','progress_color': 'green'}
            hc.progress_bar(int(max_epoch/value*100),f'Projects :  {selected_projects} still in Training, {max_epoch} / {value}',sentiment='good',override_theme=override_theme)
        except:
            st.warning("No train reslut")
    else:
        st.warning("No train reslut")


def trainpage(selected_projects):
    # st.write(selected_projects)

    with st.expander("Update yaml file for training", expanded=True):
        # 更新yaml训练配置文件
        update_yaml(selected_projects)

    with st.expander("Start train", expanded=True):
        # 训练
        train_project(selected_projects)

    with st.expander("Training", expanded=True):
        # 训练
        train_progress(selected_projects)

    with st.expander("Deploy to User App", expanded=True):
        # 部署
        deploy(selected_projects)

    with st.expander("Train Result", expanded=True):
        # 部署
        train_result_show(selected_projects)
