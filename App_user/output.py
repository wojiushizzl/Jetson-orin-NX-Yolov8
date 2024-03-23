OUTPUT=['Alarm','Rs485','Stop']
import Jetson.GPIO as GPIO
import subprocess



RelayA=[21,20,26]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RelayA, GPIO.OUT, initial=GPIO.HIGH)


def output(output_type):
    if OUTPUT.index(output_type)==0:
        alarm_script_path="alarm_run.py"
        subprocess.Popen(["python",alarm_script_path])
    if OUTPUT.index(output_type)==1:
        print('Rs485')
    if OUTPUT.index(output_type)==2:
        try:
            print("turn off")
            GPIO.output(RelayA, GPIO.LOW)
        except:
            GPIO.cleanup()