# Jetson-orin-NX-env
Run yolov8 in Jetson orin NX

```bash
git clone https://github.com/wojiushizzl/Jetson-orin-NX-env.git
```

## 1. Install Sunlogin  (optional)
[Download the Kylin Arm64 version   ](https://sunlogin.oray.com/download/linux?type=personal&ici=sunlogin_navigation) 
	
**SunloginClient_11.0.1.44968_kylin_arm.deb**

```bash
#install 
$ sudo dpkg -i SunloginClient_11.0.1.44968_kylin_arm.deb 

#start
$ /usr/local/sunlogin/bin/sunloginclient

#uninstall
$ sudo dpkg -r sunloginclient

#Set Sunlogin start with sys starting
open app "startup application"
add command "/usr/local/sunlogin/bin/sunloginclient"

$ reboot
```
## 2. pip change source

```bash
$ pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## 3. Install Archiconda instead of miniconda
reference https://blog.csdn.net/gls_nuaa/article/details/135630629

```bash
wget https://github.com/Archiconda/build-tools/releases/download/0.2.3/Archiconda3-0.2.3-Linux-aarch64.sh

#install
$ bash Archiconda3-0.2.3-Linux-aarch64.sh

#restart Terminal, check 
$ conda 

#change conda source
$ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
$ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge 
$ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
$ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/

#create conda env 
$ conda create -n yolov8 python=3.8

#activate env
$ conda activate yolov8

#remove env
$ conda remove -n yolov8 --all

```
## 4. Install nvidia-jetpack
```bash
$ sudo apt upgrade
$ sudo apt update
$ sudo apt dist-upgrade
$ sudo reboot
$ sudo apt install nvidia-jetpack 
```
## 5. Install jtop
```bash	
$ sudo apt install python3-pip
$ sudo -H pip3 install -U jetson-stats
$ sudo reboot
```

## 6. Check 
```bash
$ sudo jetson_release
```
```
Software part of jetson-stats 4.2.6 - (c) 2024, Raffaello Bonghi
Model: NVIDIA Orin NX Developer Kit - Jetpack 5.1.1 [L4T 35.3.1]
NV Power Mode[0]: MAXN
Serial Number: [XXX Show with: jetson_release -s XXX]
Hardware:
    - P-Number: p3767-0001
    - Module: NVIDIA Jetson Orin NX (8GB ram)
Platform:
    - Distribution: Ubuntu 20.04 focal
    - Release: 5.10.104-tegra
jtop:
    - Version: 4.2.6
    - Service: Active
Libraries:
    - CUDA: 11.4.315
    - cuDNN: 8.6.0.166
    - TensorRT: 8.5.2.2
    - VPI: 2.2.7
    - Vulkan: 1.3.204
    - OpenCV: 4.5.4 - with CUDA: NO
```



## 7. Install torch
[Download the torch wheel](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048)
**torch-1.8.0-cp36-cp36m-linux_aarch64.whl** 
Must check the jetpach version !!!
```bash
$ sudo apt-get -y update
$ sudo apt-get -y install autoconf bc build-essential g++-8 gcc-8 clang-8 lld-8 gettext-base gfortran-8 iputils-ping libbz2-dev libc++-dev libcgal-dev libffi-dev libfreetype6-dev libhdf5-dev libjpeg-dev liblzma-dev libncurses5-dev libncursesw5-dev libpng-dev libreadline-dev libssl-dev libsqlite3-dev libxml2-dev libxslt-dev locales moreutils openssl python-openssl rsync scons python3-pip libopenblas-dev
$ pip install 'Cython<3'
$ pip install numpy torch-1.8.0-cp36-cp36m-linux_aarch64.whl
```
**Verify**
```bash
$ python
```

```python
import torch
print(torch.__version__)
>>> 2.1.0a0+41361538.nv23.06
print(torch.cuda.is_available())
>>> True
print(torch.backends.cudnn.version())
>>> 8600
```
**Success !**
	
## 8. Install torchvision
Select the version of torchvision to download depending on the version of PyTorch that you have installed:
```
    PyTorch v1.0 - torchvision v0.2.2
    PyTorch v1.1 - torchvision v0.3.0
    PyTorch v1.2 - torchvision v0.4.0
    PyTorch v1.3 - torchvision v0.4.2
    PyTorch v1.4 - torchvision v0.5.0
    PyTorch v1.5 - torchvision v0.6.0
    PyTorch v1.6 - torchvision v0.7.0
    PyTorch v1.7 - torchvision v0.8.1
    PyTorch v1.8 - torchvision v0.9.0
    PyTorch v1.9 - torchvision v0.10.0
    PyTorch v1.10 - torchvision v0.11.1
    PyTorch v1.11 - torchvision v0.12.0
    PyTorch v1.12 - torchvision v0.13.0
    PyTorch v1.13 - torchvision v0.13.0
    PyTorch v1.14 - torchvision v0.14.1
    PyTorch v2.0 - torchvision v0.15.1
    PyTorch v2.1 - torchvision v0.16.1  <--
```
```bash
#Install
$ sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libopenblas-dev libavcodec-dev libavformat-dev libswscale-dev
$ git clone --branch v0.16.1 https://github.com/pytorch/vision torchvision
$ cd torchvision
$ export BUILD_VERSION=0.16.1  # where 0.x.0 is the torchvision version  
$ python3 setup.py install --user
$ cd ../  # attempting to load torchvision from build dir will result in import error
$ pip install 'pillow<7' # always needed for Python 2.7, not needed torchvision v0.5.0+ with Python 3.6
```
```bash
#Verify
$ python

import torchvision
print(torchvision.__version__)
```

## 9. Install yolov8
```bash
$ pip install ultralytics
```
## 10. Install streamlit  etc. (optional)
```bash	
$ pip install streamlit
$ pip install -U streamlit-webrtc
$ pip install playsound
$ pip install -U hydralit_components
$ pip install ruamel.yaml
$ pip install streamlit-extras
$ pip install streamlit_card
$ pip install streamlit-option-menu
```

## 11. Install VSCode  (optional)
[Download arm64 version "code_1.87.2-1709911730_arm64.deb"](https://code.visualstudio.com/docs/?dv=linuxarm64_deb)
```bash
#Install
$ sudo dpkg -i code_1.87.2-1709911730_arm64.deb
```

## 12. Install labelimg  (optional)

https://github.com/HumanSignal/labelImg
```bash
#install 
conda create -n labelimg
conda activate labelimg
conda install pyqt=5
conda install -c anaconda lxml
pyrcc5 -o libs/resources.py resources.qrc

#run labelimg
python labelImg.py
python labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

```
## 13. Install label-studio  (optional)
[Label studio github](https://github.com/HumanSignal/label-studio?tab=readme-ov-file)

```bash
#Install with conda
conda create --name label-studio
conda activate label-studio
conda install psycopg2
pip install label-studio

#run 
label-studio
```



## 13. Run yolov8 demo

```bash
#run simple demo for predict single image
cd JETSON-ORIN-NX-ENV
cd demo
conda activate yolov8
python yolov8_demo.py
```
```bash
#run webapp demo  user model
cd JETSON-ORIN-NX-ENV
cd App_user
conda activate yolov8
streamlit run app.py
```
```bash
#run webapp demo  develop model
cd JETSON-ORIN-NX-ENV
cd App_dev
conda activate yolov8
streamlit run dev.py
```

## *. others
```bash
#check system version 
$ lsb_release -a
#No LSB modules are available.
#Distributor ID:	Ubuntu
#Description:	Ubuntu 20.04.6 LTS
#Release:	20.04
#Codename:	focal

#check system architecture
$ dpkg --print-architecture
#arm64

#check jetpack version
$ sudo apt-cache show nvidia-jetpack

#check LT4 version
$ cat /etc/nv_tegra_release 
# R35 (release), REVISION: 3.1, GCID: 32827747, BOARD: t186ref, EABI: aarch64, DATE: Sun Mar 19 15:19:21 UTC 2023
```


