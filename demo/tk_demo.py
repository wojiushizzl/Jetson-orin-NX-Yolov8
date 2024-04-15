from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading


class VideoStreamApp:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        self.vid = cv2.VideoCapture(self.video_source)

        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH) / 2)
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)
        self.canvas = tk.Canvas(
            window,
            width=self.width,
            height=self.height
        )
        self.canvas.pack()

        self.ifShot = False
        self.btn_snapshot = tk.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack()

        self.ifPre = False
        self.btn_openYolo = tk.Button(window, text="Yolo", width=50, command=self.openYolo)
        self.btn_openYolo.pack()


        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        self.thread.start()

        self.window.mainloop()

    def openYolo(self):
        self.ifPre = not self.ifPre

    def snapshot(self):
        self.ifShot = True

    def update(self):
        while True:
            ret, frame = self.vid.read()
            if ret:
                frame = cv2.resize(frame, (self.width, self.height))
                if self.ifPre:
                    print('Open Yolo')
                    results = model(frame)
                    frame = results[0].plot()
                if self.ifShot:
                    print('Take photo')
                    cv2.imwrite("snapshot.png", frame)
                    self.ifShot = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)



                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


# Create a window and pass it to the VideoStreamApp class
VideoStreamApp(tk.Tk(), "Video Stream App")
