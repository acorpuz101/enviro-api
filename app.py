from flask import Flask
import json
import time
import colorsys
import os
import sys
import ST7735
from subprocess import PIPE, Popen
try:
     # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280
from fonts.ttf import RobotoMedium as UserFont
import logging

app = Flask(__name__)
bme280 = BME280()

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    try:
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
        output, _error = process.communicate()
        return float(output[output.index('=') + 1:output.rindex("'")])
    except:
        return float(0)

# temperature down, and increase to adjust up
factor = 2.25


@app.route('/')
def hello_world():
        return 'Hello, World!'

@app.route('/status')
def getStatus():
    cpu_temp = get_cpu_temperature()
    cpu_temps = [get_cpu_temperature()] * 5
    cpu_temps = cpu_temps[1:] + [cpu_temp]
    avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps)) 
    raw_temp = bme280.get_temperature()

    tempC = raw_temp - ((avg_cpu_temp - raw_temp) / factor)

    dataTemp = (tempC * 1.8) + 32
    dataPressure = bme280.get_pressure()
    dataHumidity = bme280.get_humidity()
    data = {
        "tempC": "{:.2f}".format(tempC),
        "tempF": "{:.2f}".format(dataTemp),
        "pressure": "{:.2f}".format(dataPressure),
        "humidity": "{:.2f}".format(dataHumidity),
        "avgCpuTemp": "{:.2f}".format(avg_cpu_temp),
        "cpuTemp": "{:.2f}".format(cpu_temp)
        }
    jsonData = json.dumps(data)
    return jsonData

@app.route('/temp')
def displayTemp():
    raw_temp = bme280.get_temperature()
    #dataTemp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
    #dataTemp = (dataTemp * 1.8) + 32
    dataTemp = (raw_temp * 1.8) + 32
    return "{}: {:.1f} {}".format("temperature"[:4], dataTemp, "F")

@app.route('/humidity')
def displayHumidity():
    dataHumidity = bme280.get_humidity()
    return "{}: {:.1f} {}".format("Humidity", dataHumidity, "%")

@app.route('/pressure')
def displayPressure():
    dataPressure = bme280.get_pressure()
    return "{}: {:.1f} {}".format("Pressure", dataPressure, "hPa")


