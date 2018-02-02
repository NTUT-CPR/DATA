import os
import json
import time
import urllib.request

def getWeatherData():
    json_file = os.path.dirname(os.path.abspath(__file__)) + "/weather_data/data.json"
    timestamp_file = os.path.dirname(os.path.abspath(__file__)) + "/weather_data/timestamp.json"
    with open(timestamp_file, "r", encoding="utf-8") as fp:
        timestamp = float(fp.read())

    now = time.time()
    if now - timestamp < 1800:
        #一小時內
        json_data = ""
        with open(json_file, "r", encoding="utf-8") as fp:
            json_data = json.loads(fp.read(), encoding="utf-8")
        return json_data
    
    print("reload CWB Data!!!")
    req = urllib.request.Request('http://opendata.epa.gov.tw/ws/Data/ATM00698/?$skip=0&$top=114&format=json&token=c1pj0s/ZMUK1PckVAvMVWA')
    cwb_data = ""
    with urllib.request.urlopen(req) as response:
        cwb_data = response.read()
    cwb_data = cwb_data.decode("utf-8")
    with open(json_file, "w", encoding="utf-8") as fp:
        fp.write(cwb_data)

    with open(timestamp_file, "w", encoding="utf-8") as fp:
        fp.write(str(time.time()))

    return json.loads(cwb_data, encoding="utf-8")

def getAQIData():
    json_file = os.path.dirname(os.path.abspath(__file__)) + "/aqi_data/data.json"
    timestamp_file = os.path.dirname(os.path.abspath(__file__)) + "/aqi_data/timestamp.json"
    with open(timestamp_file, "r", encoding="utf-8") as fp:
        timestamp = float(fp.read())

    now = time.time()
    if now - timestamp < 1800:
        #一小時內
        json_data = ""
        with open(json_file, "r", encoding="utf-8") as fp:
            json_data = json.loads(fp.read(), encoding="utf-8")
        return json_data
    
    print("reload AQI Data!!!")
    req = urllib.request.Request('http://opendata.epa.gov.tw/ws/Data/ATM00679/?$skip=0&$top=114&format=json&token=c1pj0s/ZMUK1PckVAvMVWA')
    cwb_data = ""
    with urllib.request.urlopen(req) as response:
        cwb_data = response.read()
    cwb_data = cwb_data.decode("utf-8")
    with open(json_file, "w", encoding="utf-8") as fp:
        fp.write(cwb_data)

    with open(timestamp_file, "w", encoding="utf-8") as fp:
        fp.write(str(time.time()))

    return json.loads(cwb_data, encoding="utf-8")

def getUVData():
    json_file = os.path.dirname(os.path.abspath(__file__)) + "/uv_data/data.json"
    timestamp_file = os.path.dirname(os.path.abspath(__file__)) + "/uv_data/timestamp.json"
    with open(timestamp_file, "r", encoding="utf-8") as fp:
        timestamp = float(fp.read())

    now = time.time()
    if now - timestamp < 1800:
        #一小時內
        json_data = ""
        with open(json_file, "r", encoding="utf-8") as fp:
            json_data = json.loads(fp.read(), encoding="utf-8")
        return json_data
    
    print("reload UV Data!!!")
    req = urllib.request.Request('http://opendata2.epa.gov.tw/UV/UV.json?token=c1pj0s/ZMUK1PckVAvMVWA')
    cwb_data = ""
    with urllib.request.urlopen(req) as response:
        cwb_data = response.read()
    cwb_data = cwb_data.decode("utf-8")
    with open(json_file, "w", encoding="utf-8") as fp:
        fp.write(cwb_data)

    with open(timestamp_file, "w", encoding="utf-8") as fp:
        fp.write(str(time.time()))

    return json.loads(cwb_data, encoding="utf-8")

def rootId2Str(root_id):
    data = {
        0: '臺北', 
        1: '板橋'}
    if data[root_id] is None:
        return '臺北'
    return data[root_id]