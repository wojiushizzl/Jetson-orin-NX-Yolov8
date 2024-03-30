from ultralytics import YOLO
from multiprocessing import Process, freeze_support
import os


def train(
        name='test',
        project_name="test",#保存训练结果的项目目录名称。允许有组织地存储不同的实验。
        epochs=50, #训练历元总数。每个历元代表对整个数据集进行一次完整的训练。调整该值会影响训练时间和模型性能。
        batch=2, #训练的批量大小，表示在更新模型内部参数之前要处理多少张图像。自动批处理 (batch=-1)会根据 GPU 内存可用性动态调整批处理大小。
        patience=20,#在验证指标没有改善的情况下，提前停止训练所需的历元数。当性能趋于平稳时停止训练，有助于防止过度拟合。
        exist_ok=False,#如果为 True，则允许覆盖现有的项目/名称目录。这对迭代实验非常有用，无需手动清除之前的输出。
        single_cls=False,#在训练过程中将多类数据集中的所有类别视为单一类别。适用于二元分类任务，或侧重于对象的存在而非分类。
        imgsz=640, # 用于训练的目标图像尺寸。所有图像在输入模型前都会被调整到这一尺寸。影响模型精度和计算复杂度。
        degrees=20,#float -180 - +180  在指定的度数范围内随机旋转图像，提高模型识别不同方向物体的能力。
        translate=0.1,#float  0.0 - 1.0	以图像大小的一小部分水平和垂直平移图像，帮助学习检测部分可见的物体。
        scale=0.5,# float 0.0 - 1.0  通过增益因子缩放图像，模拟物体与摄像机的不同距离。
        flipud=0,# float  0.0 - 1.0 以指定的概率将图像翻转过来，在不影响物体特征的情况下增加数据的可变性。
        fliplr=0,# float 0.0 - 1.0  以指定的概率将图像从左到右翻转，这对学习对称物体和增加数据集多样性非常有用。
        erasing=0.4, # float 0.0 - 1.0  在分类训练过程中随机擦除部分图像，鼓励模型将识别重点放在不明显的特征上。
        mosaic=1.0, # float  0.0 - 1.0将四幅训练图像合成一幅，模拟不同的场景构成和物体互动。对复杂场景的理解非常有效。
        mixup=0,# float 0.0 - 1.0  混合两幅图像及其标签，创建合成图像。通过引入标签噪声和视觉变化，增强模型的泛化能力。
        copy_paste=0,#float 0.0 - 1.0  从一幅图像中复制物体并粘贴到另一幅图像上，用于增加物体实例和学习物体遮挡。
        auto_augment='randaugment', #自动应用预定义的增强策略 (randaugment, autoaugment, augmix)，通过丰富视觉特征来优化分类任务。
):
    project_path = os.path.join('projects', project_name)
    yaml_path = os.path.join(project_path, 'train.yaml')
    result_path = os.path.join(project_path, 'train')
    # Load a model
    model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)
    # Train the model
    results = model.train(
        name=name,
        data=yaml_path,
        project=result_path,
        epochs=epochs,
        batch=batch,
        patience=patience,
        exist_ok=exist_ok,
        single_cls=single_cls,
        imgsz=imgsz,
        degrees=degrees,
        translate=translate,
        scale=scale,
        flipud=flipud,
        fliplr=fliplr,
        erasing=erasing,
        mosaic=mosaic,
        mixup=mixup,
        copy_paste=copy_paste,
        auto_augment=auto_augment,
        plots=True,
    )


if __name__ == "__main__":
    freeze_support()

    p = Process(target=train)
    p.start()
    p.join()
