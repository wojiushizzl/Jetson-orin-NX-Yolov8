import Jetson.GPIO as GPIO
import subprocess

OUTPUT = ['Alarm', 'Rs485', 'Stop','Reset']

RelayA = [21, 20, 26]


def output(output_type):
    if OUTPUT.index(output_type) == 0:
        alarm_script_path = "alarm_run.py"
        subprocess.Popen(["python", alarm_script_path])
    if OUTPUT.index(output_type) == 1:
        print('Rs485')
    if OUTPUT.index(output_type) == 2:
        GPIO.output(RelayA, GPIO.LOW)

    if OUTPUT.index(output_type) == 3:
        GPIO.output(RelayA, GPIO.HIGH)

