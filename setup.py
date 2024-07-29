import os
import shutil
import ruamel.yaml
import subprocess

current_path = os.getcwd()

logo_path = os.path.abspath('./setup/logo.png')
dev_logo_path=os.path.abspath('./setup/dev_logo.png')
desktop_logo_path=os.path.abspath('./setup/desktop_logo.png')




user_sh_path = os.path.abspath('./setup/start.sh')
dev_sh_path=os.path.abspath('./setup/dev.sh')
desktop_sh_path=os.path.abspath('./setup/desktop.sh')



dt_path = os.path.abspath('./setup/STARTAPP.desktop')
dev_dt_path = os.path.abspath('./setup/DEVAPP.desktop')
desktop_dt_path = os.path.abspath('./setup/DesktopAPP.desktop')




userapp_path = os.path.abspath('./App_user')
devapp_path = os.path.abspath('./App_dev')
desktopapp_path = os.path.abspath('./App_desktop')





usr_path=os.listdir('/home')
print(f"usr name :{usr_path[0]}")
init_tran_yaml_path=os.path.join('/home',usr_path[0],'.config','Ultralytics','settings.yaml')

print(current_path)
print(logo_path)
print(user_sh_path)
print(userapp_path)
print(devapp_path)
print(dt_path)


#  add Permission  /usr/share/applications/
subprocess.run(['sudo','chmod','777','/usr/share/applications/'])


# modify start.sh file
with open(user_sh_path, 'r') as f:
    sh_lines = f.readlines()

cd_command = 'cd ' + userapp_path + '\n'
for i in range(len(sh_lines)):
    if 'cd' in sh_lines[i]:
        sh_lines[i] = cd_command

try:
    condash_path=subprocess.run(['sudo','find','/','-name','conda.sh'],stdout=subprocess.PIPE)
    condash_path=condash_path.stdout.decode('utf-8')
    source_command='source '+condash_path +'\n'

    for i in range(len(sh_lines)):
        if 'source' in sh_lines[i]:
            sh_lines[i] = source_command
except:
    print('No conda detected !')

with open(user_sh_path, 'w') as f:
    f.writelines(sh_lines)

# modify dev.sh file
with open(dev_sh_path, 'r') as f:
    sh_lines = f.readlines()

cd_command = 'cd ' + devapp_path + '\n'
for i in range(len(sh_lines)):
    if 'cd' in sh_lines[i]:
        sh_lines[i] = cd_command

try:
    # condash_path=subprocess.run(['find','/','-name','conda.sh'],stdout=subprocess.PIPE)
    # condash_path=condash_path.stdout.decode('utf-8')
    source_command='source '+condash_path +'\n'

    for i in range(len(sh_lines)):
        if 'source' in sh_lines[i]:
            sh_lines[i] = source_command
except:
    print('No conda detected !')

with open(dev_sh_path, 'w') as f:
    f.writelines(sh_lines)


# modify desktop.sh file
with open(desktop_sh_path, 'r') as f:
    sh_lines = f.readlines()

cd_command = 'cd ' + desktopapp_path + '\n'
for i in range(len(sh_lines)):
    if 'cd' in sh_lines[i]:
        sh_lines[i] = cd_command

try:
    # condash_path=subprocess.run(['find','/','-name','conda.sh'],stdout=subprocess.PIPE)
    # condash_path=condash_path.stdout.decode('utf-8')
    source_command='source '+condash_path +'\n'

    for i in range(len(sh_lines)):
        if 'source' in sh_lines[i]:
            sh_lines[i] = source_command
except:
    print('No conda detected !')

with open(desktop_sh_path, 'w') as f:
    f.writelines(sh_lines)




# modify STARTAPP.desktop file
with open(dt_path, 'r') as f:
    dt_lines = f.readlines()

EXEkey = 'Exec=bash '
iconkey = 'Icon='

for i in range(len(dt_lines)):
    if dt_lines[i].startswith(EXEkey):
        dt_lines[i] = EXEkey + user_sh_path + '\n'
    if dt_lines[i].startswith(iconkey):
        dt_lines[i] = iconkey + logo_path + '\n'

with open(dt_path, 'w') as f:
    f.writelines(dt_lines)
# modify DEVAPP.desktop file
with open(dev_dt_path, 'r') as f:
    dt_lines = f.readlines()

EXEkey = 'Exec=bash '
iconkey = 'Icon='

for i in range(len(dt_lines)):
    if dt_lines[i].startswith(EXEkey):
        dt_lines[i] = EXEkey + dev_sh_path + '\n'
    if dt_lines[i].startswith(iconkey):
        dt_lines[i] = iconkey + dev_logo_path + '\n'

with open(dev_dt_path, 'w') as f:
    f.writelines(dt_lines)

# modify DesktopAPP.desktop file
with open(desktop_dt_path, 'r') as f:
    dt_lines = f.readlines()

EXEkey = 'Exec=bash '
iconkey = 'Icon='

for i in range(len(dt_lines)):
    if dt_lines[i].startswith(EXEkey):
        dt_lines[i] = EXEkey + desktop_sh_path + '\n'
    if dt_lines[i].startswith(iconkey):
        dt_lines[i] = iconkey + desktop_logo_path + '\n'

with open(desktop_dt_path, 'w') as f:
    f.writelines(dt_lines)





# copy .desktop to /usr/share/applications/
app_dir = '/usr/share/applications'

shutil.copy(dt_path, app_dir)

shutil.copy(dev_dt_path, app_dir)

shutil.copy(desktop_dt_path, app_dir)




# modify init yaml path at usr/home/.config/ultralytics
yaml = ruamel.yaml.YAML()
# 读取复制的文件并更改其中一行代码
with open(init_tran_yaml_path, "r", encoding="utf-8") as file:
    lines = yaml.load(file)

if "datasets_dir" in lines:
    lines["datasets_dir"] = devapp_path

# 将更改后的内容写回文件
with open(init_tran_yaml_path, "w", encoding="utf-8") as file:
    yaml.dump(lines, file)
