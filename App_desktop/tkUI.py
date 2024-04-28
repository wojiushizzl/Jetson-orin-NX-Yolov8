import tkinter as tk
from tkinter import ttk
# from PIL import Image,ImageTk
# import ctypes                   #可让python与C语言混合使用
#告诉操作系统使用程序自身的dpi适配
# ctypes.windll.shcore.SetProcessDpiAwareness(1)
import cv2
from PIL import Image, ImageTk
import threading
import uuid
from ultralytics import YOLO
import configparser
from tkinter import filedialog
import Jetson.GPIO as GPIO
from logic_check import logic_check
from output import output


RelayA = [21, 20, 26]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RelayA, GPIO.OUT, initial=GPIO.LOW)


class mytkinter(tk.Tk):
    width=800
    height=600
    ROW=10
    COL=10
    first_load=True
    # def __init__(self):
    #     super().__init__()

    def setupUi(self):
        self.config(bg='#666888', bd=0)
        self.title("YOLOv8 检测")
        screen_width = self.winfo_screenwidth()  # 电脑屏幕宽度
        screen_height = self.winfo_screenheight()
        print(screen_width, screen_height)
        center_geometry = [int(screen_width / 2 - self.width / 2), int(screen_height / 2 - self.height / 2)]
        geometry_str = "{}x{}+{}+{}".format(self.width, self.height, center_geometry[0], center_geometry[1])
        print(geometry_str)
        self.geometry(geometry_str)

        # 配置信息
        self.config = configparser.ConfigParser()
        self.load_config()

        # 画布
        self.cv = tk.Canvas(self, bg='snow')

        # self.style_1=ttk.Style()
        # self.style_1.configure("TLabel",foreground='black',background='ivory')
        self.tab_main = ttk.Notebook(self.cv)
        # self.tab_main.pack(expand=1,fill='both')#这段代码很重要


        self.tab1 = tk.Frame(self.tab_main, bg='snow')
        self.tab1.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.9)
        self.tab_main.add(self.tab1, text='图像检测')

        self.tab2 = tk.Frame(self.tab_main, bg='ivory')
        self.tab2.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.9)
        self.tab_main.add(self.tab2, text='视频检测')

        self.tab3 = tk.Frame(self.tab_main, bg='#eeebbb')
        self.tab3.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.9)
        self.tab_main.add(self.tab3, text='摄像头检测')

        self.tab4 = tk.Frame(self.tab_main, bg='#666888')
        self.tab4.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.9)
        self.tab_main.add(self.tab4, text='设置')

        #tab1
        self.VLabel1 = self.myViewLabel(self.tab1, 0.005, 0.01, 0.49, 0.99)
        self.VLabel2 = self.myViewLabel(self.tab1, 0.505, 0.01, 0.49, 0.99)

        # tab2
        self.VLabel3 = self.myViewLabel(self.tab2, 0.005, 0.01, 0.49, 0.99)
        self.VLabel4 = self.myViewLabel(self.tab2, 0.505, 0.01, 0.49, 0.99)

        # tab3
        self.VLabel5 = self.myViewLabel(self.tab3, 0.005, 0.01, 0.99, 0.99)
        # self.VLabel6 = self.myViewLabel(self.tab3, 0.505, 0.01, 0.49, 0.99)


        self.ifstart=False
        self.btn_start=tk.Button(self.VLabel5,text='START',bd=0,bg='black',fg='white',command=self.start)
        self.btn_start.place(relx=0.01,rely=0.05,width=100,height=30)

        # tab4
        self.btn1=tk.Button(self.tab4,text='选择权重',bd=0,bg='black',fg='white',command=self.open_model_file)
        self.btn1.place(relx=0.01,rely=0.05,width=100,height=30)
        self.var1=tk.StringVar()
        self.entry1=tk.Entry(self.tab4,textvariable=self.var1)
        self.entry1.place(relx=0.01,x=105,rely=0.05,relwidth=0.98,width=-105,height=30)
        self.var1.set(self.weight)

        self.label2 = tk.Label(self.tab4, text="图片大小",bd=0,bg='black',fg='white')
        self.label2.place(relx=0.01,rely=0.05,y=50,width=100,height=30)
        self.var2=tk.StringVar()
        self.entry2=tk.Entry(self.tab4,textvariable=self.var2)
        self.entry2.place(relx=0.01,x=105,rely=0.05,y=50,relwidth=0.48,width=-105,height=30)
        self.var2.set(self.imgsz)

        self.label3 = tk.Label(self.tab4, text="置信度阈值", bd=0, bg='black', fg='white')
        self.label3.place(relx=0.51, rely=0.05, y=50, width=100, height=30)
        self.var3 = tk.StringVar()
        self.entry3 = tk.Entry(self.tab4, textvariable=self.var3)
        self.entry3.place(relx=0.51, x=105, rely=0.05, y=50, relwidth=0.48, width=-105, height=30)
        self.var3.set(self.conf)

        self.label4 = tk.Label(self.tab4, text="iou阈值", bd=0, bg='black', fg='white')
        self.label4.place(relx=0.01, rely=0.05, y=100, width=100, height=30)
        self.var4 = tk.StringVar()
        self.entry4 = tk.Entry(self.tab4, textvariable=self.var4)
        self.entry4.place(relx=0.01, x=105, rely=0.05, y=100, relwidth=0.48, width=-105, height=30)
        self.var4.set(self.iou)

        self.label5 = tk.Label(self.tab4, text="目标最大数", bd=0, bg='black', fg='white')
        self.label5.place(relx=0.51, rely=0.05, y=100, width=100, height=30)
        self.var5 = tk.StringVar()
        self.entry5 = tk.Entry(self.tab4, textvariable=self.var5)
        self.entry5.place(relx=0.51, x=105, rely=0.05, y=100, relwidth=0.48, width=-105, height=30)
        self.var5.set(self.max_det)

        self.label6 = tk.Label(self.tab4, text="检测设备选择", bd=0, bg='black', fg='white')
        self.label6.place(relx=0.01, rely=0.05, y=150, width=100, height=30)
        self.var6 = tk.StringVar()
        self.entry6 = tk.Entry(self.tab4, textvariable=self.var6)
        self.entry6.place(relx=0.01, x=105, rely=0.05, y=150, relwidth=0.48, width=-105, height=30)
        self.var6.set(self.device)
        self.btn2=tk.Button(self.tab4,text="保存设置", bd=0, bg='black', fg='white',command=self.save_config)
        self.btn2.place(relx=0.51, rely=0.05, y=150, relwidth=0.48, height=30)

        #启用摄像头获取
        self.vid = cv2.VideoCapture(int(self.var6.get()))

        #load model
        self.load_model()

        #onclose
        self.protocol('WM_DELETE_WINDOW',self.__del__)


        
    # 保存配置到文件
    def save_config(self):
        with open('app_config.ini', 'w') as configfile:
            self.config['Settings'] = {
                'weight': self.var1.get(),
                'imgsz': self.var2.get(),
                'conf': self.var3.get(),
                'iou': self.var4.get(),
                'max_det': self.var5.get(),
                'device': self.var6.get(),
                }
            self.config.write(configfile)
            print('Settings saved')

    def init_config(self):
        with open('app_config.ini', 'w') as configfile:
            self.config.write(configfile)
            print('Settings initialed')

    # 加载配置信息
    def load_config(self):
        print(self.config.read('app_config.ini'))
        if self.config.read('app_config.ini'):
            self.settings = self.config['Settings']
        else:
            self.config['Settings'] = {
                'weight': 'yolov8n.pt',
                'imgsz': '640',
                'conf': '0.5',
                'iou': '0.45',
                'max_det': '100',
                'device': '0',
                }
            self.settings = self.config['Settings']
            self.init_config()

        self.weight = self.settings['weight']
        self.imgsz = self.settings['imgsz']
        self.conf = self.settings['conf']
        self.iou = self.settings['iou']
        self.max_det = self.settings['max_det']
        self.device = self.settings['device']

    def myViewLabel(self,master,relx,rely,relwidth,relheight):#自定义标签，用于显示图片，可实现图片的放大缩小
        label=tk.Label(master,bg='#666888',bd=0)
        label.place(relx=relx,rely=rely,relwidth=relwidth,relheight=relheight)
        # self.label.bind("<Double-Button-1>",lambda a:mytkinter().show_toplevel(self))
        return label


    def start(self):
        self.ifstart=not self.ifstart
        if self.ifstart:
            self.btn_start.config(background='green',text='END')
            self.update_view()
        else:
            self.btn_start.config(background='black',text='START')

    def puttext(self,text, res_plotted, color):
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


    def update_view(self):
        ret, frame = self.vid.read()
        # print('Open Yolo')

        if ret and self.ifstart:
            frame = cv2.resize(frame, (self.width, self.height))
            res = self.model.predict(
                frame,
                conf=float(self.var3.get()),
                imgsz=int(self.var2.get()),
                iou=float(self.var4.get()),
                max_det=int(self.var5.get()),
                classes=[0], 
                )
            
            boxes = res[0].boxes
            check = logic_check("Detected -> OUTPUT", boxes)
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
            self.puttext(result, res_plotted, color)


            frame = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.VLabel5.imgtk = imgtk
            self.VLabel5.config(image=imgtk)
            self.after(1, self.update_view)
        else:
            return


    def open_model_file(self):
        self.weight=filedialog.askopenfilename()
        self.var1.set(self.weight)
        self.load_model()


    def load_model(self):
        #load model
        print(f"load model : {self.var1.get()}")
        self.model = YOLO(self.var1.get())



    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        GPIO.output(RelayA, GPIO.LOW)
        self.destroy()
