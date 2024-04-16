from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading
import uuid


class VideoStreamApp:
    def __init__(self, window, window_title, video_source=1):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        self.vid = cv2.VideoCapture(self.video_source)

        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH) / 2)
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)
        print(self.width)
        print(self.height)
        self.panel = tk.Label(self.window,text='画面',width=self.width,height=self.height)  # initialize image panel
        self.panel.grid(column=0,row=0,rowspan=10)
        self.window.config(cursor="arrow")



        self.ifShot = False
        self.btn_snapshot = tk.Button(window, text="Snapshot", height=10,width=50, command=self.snapshot)
        self.btn_snapshot.grid(column=1,row=0,columnspan=2,rowspan=2)

        self.ifPre = False
        self.btn_openYolo = tk.Button(window, text="Yolo", height=10,width=50, command=self.openYolo)
        self.btn_openYolo.grid(column=1,row=2,columnspan=2,rowspan=2)


        self.update()

        self.window.mainloop()



    def openYolo(self):
        self.ifPre = not self.ifPre

    def snapshot(self):
        self.ifShot = True

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.resize(frame, (self.width, self.height))
            if self.ifPre:
                print('Open Yolo')
                results = model(frame,conf=0.5)
                frame = results[0].plot()
            if self.ifShot:
                print('Take photo')
                img_name=str(uuid.uuid4()) + ".png"
                cv2.imwrite("./images/"+img_name, frame)
                self.ifShot = False


            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)
            self.window.after(1, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


# Create a window and pass it to the VideoStreamApp class
VideoStreamApp(tk.Tk(), "Video Stream App")
