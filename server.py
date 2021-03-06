import os
import glob
import time
import random
from flask import Flask, render_template, jsonify
app = Flask(__name__)

ACCURACY = 1

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

def format_temp(temp, digits):
    return u'{number:.{digits}f}'.format(number=temp, digits=digits)

@app.context_processor
def utility_processor():
    return dict(format_temp=format_temp)

@app.route("/")
def hello():
    temp = read_temp()[1]
    klass = get_temp_sentiment(temp)

    return render_template('hello.html', temp=temp, klass=klass, accuracy=ACCURACY)

@app.route("/update")
def update():
    temp = format_temp(read_temp()[1], ACCURACY)
    klass = get_temp_sentiment(temp)

    return jsonify(temp=temp, klass=klass)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)