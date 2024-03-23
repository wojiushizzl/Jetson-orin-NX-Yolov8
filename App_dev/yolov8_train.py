from ultralytics import YOLO
from multiprocessing import Process, freeze_support
import os


def train(project_name="test",epochs=50,batch=2):
    project_path=os.path.join('projects',project_name)
    yaml_path=os.path.join(project_path,'train.yaml')
    result_path=os.path.join(project_path,'train')
    # Load a model
    model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)
    # Train the model
    results = model.train(
        data=yaml_path,
        project=result_path,
        epochs=epochs,
        batch=batch,
        imgsz=640)


if __name__ =="__main__":
    freeze_support()

    p=Process(target=train)
    p.start()
    p.join()