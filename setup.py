import os
import shutil
import ruamel.yaml


current_path = os.getcwd()

logo_path = os.path.abspath('./setup/logo.png')

sh_path = os.path.abspath('./setup/start.sh')

dt_path = os.path.abspath('./setup/STARTAPP.desktop')

userapp_path = os.path.abspath('./App_user')

devapp_path = os.path.abspath('./App_dev')


usr_path=os.listdir('/home')
print(f"usr name :{usr_path[0]}")
init_tran_yaml_path=os.path.join('/home',usr_path[0],'.config','Ultralytics','settings.yaml')

print(current_path)
print(logo_path)
print(sh_path)
print(userapp_path)
print(devapp_path)
print(dt_path)

# modify .sh file
with open(sh_path, 'r') as f:
    sh_lines = f.readlines()

cd_command = 'cd ' + userapp_path + '\n'

for i in range(len(sh_lines)):
    if 'cd' in sh_lines[i]:
        sh_lines[i] = cd_command

with open(sh_path, 'w') as f:
    f.writelines(sh_lines)

# modify .desktop file
with open(dt_path, 'r') as f:
    dt_lines = f.readlines()

EXEkey = 'Exec=bash '
iconkey = 'Icon='

for i in range(len(dt_lines)):
    if dt_lines[i].startswith(EXEkey):
        dt_lines[i] = EXEkey + sh_path + '\n'
    if dt_lines[i].startswith(iconkey):
        dt_lines[i] = iconkey + logo_path + '\n'

with open(dt_path, 'w') as f:
    f.writelines(dt_lines)

# copy .desktop to /usr/share/applications/
app_dir = '/usr/share/applications'

shutil.copy(dt_path, app_dir)

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
