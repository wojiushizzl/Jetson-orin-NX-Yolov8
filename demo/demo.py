from ultralytics import YOLO
from jetson_utils import videoSource,videoOutput,cudaToNumpy,cudaFromNumpy
import torch
import torchvision

print(torch.__version__)
print(torchvision.__version__)

model = YOLO('yolov8n.pt')
camera=videoSource('/dev/video0')
display=videoOutput('display://0')

while display.IsStreaming():
    cuda_img=camera.Capture()
    if cuda_img is None:
        continue
    array_img=cudaToNumpy(cuda_img)
    res=model.predict(array_img,conf=0.5)
    array_res=res[0].plot()
    cuda_res=cudaFromNumpy(array_res)

    display.Render(cuda_res)
    display.SetStatus("YOLOV8 DEECTION ")


