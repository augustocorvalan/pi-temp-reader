import os
import glob
import time
from flask import Flask
app = Flask(__name__)


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#constructing the folder where the temp info is available
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#read in everything from a file
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

#returns warm, luke, or cold based on the temperature in Farenheit
def get_temp_sentiment(temp):
    warm = 65
    cold = 45
    ret = "cold"
    if temp >= warm:
        ret = "warm"
    elif temp >= cold:
        ret = "luke"

    return ret

@app.route("/")
def hello():
	return "%10.3f C, %10.3f F" % read_temp()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)