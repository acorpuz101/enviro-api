from flask import Flask
import json
import time
import colorsys
import os
import sys
import ST7735
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

@app.route('/')
def hello_world():
        return 'Hello, World!'

@app.route('/status')
def getStatus():
    raw_temp = bme280.get_temperature()
    dataTemp = (raw_temp * 1.8) + 32
    dataPressure = bme280.get_pressure()
    dataHumidity = bme280.get_humidity()
    data = {
        "tempC": "{:.1f}".format(raw_temp),
        "tempF": "{:.1f}".format(dataTemp),
        "pressure": "{:.1f}".format(dataPressure),
        "humidity": "{:.1f}".format(dataHumidity)
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


