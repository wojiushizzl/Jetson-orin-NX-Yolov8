import os
import shutil

current_path=os.getcwd()

logo_path=os.path.abspath('./setup/logo.png')

sh_path=os.path.abspath('./setup/start.sh')

dt_path=os.path.abspath('./setup/STARTAPP.desktop')
userapp_path=os.path.abspath('./App_user')
devapp_path=os.path.abspath('./App_dev')

print(current_path)
print(logo_path)
print(sh_path)
print(userapp_path)
print(devapp_path)
print(dt_path)

# modify .sh file
with open(sh_path,'r') as f:
    sh_lines=f.readlines()

cd_command='cd '+userapp_path+'\n'

for i in range(len(sh_lines)):
    if 'cd' in sh_lines[i]:
        sh_lines[i]=cd_command


with open(sh_path,'w') as f:
    f.writelines(sh_lines)


# modify .desktop file
with open(dt_path,'r') as f:
    dt_lines=f.readlines()

EXEkey='Exec=bash '
iconkey='Icon='

for i in range(len(dt_lines)):
    if dt_lines[i].startswith(EXEkey):
        dt_lines[i]=EXEkey+sh_path+'\n'
    if dt_lines[i].startswith(iconkey):
        dt_lines[i]=iconkey+logo_path+'\n'

with open(dt_path,'w') as f:
    f.writelines(dt_lines)


# copy .desktop to /usr/share/applications/
app_dir='/usr/share/applications'

shutil.copy(dt_path,app_dir)