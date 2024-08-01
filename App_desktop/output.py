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
        try:
            GPIO.output(RelayA[0], GPIO.LOW)
        except:
            try:
                GPIO.output(RelayA[1], GPIO.LOW)
            except:
                GPIO.output(RelayA[2], GPIO.LOW)


    if OUTPUT.index(output_type) == 3:
        try:
            GPIO.output(RelayA[0], GPIO.HIGH)
        except:
            try:
                GPIO.output(RelayA[1], GPIO.HIGH)
            except:
                GPIO.output(RelayA[2], GPIO.HIGH)

