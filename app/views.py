from app import app
from flask import render_template, flash, redirect, url_for, request, Response
import json
import os
import collections
import operator

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/update", methods=["GET", "POST"])
def update():
    data = '{"data": "hello"}'
    if request.method == "POST":
        accelerometer_data = request.json["accelerometer"]
        for value in accelerometer_data:
            update_json("accelerometer", value)
        temperature_data = request.json["temperature"]
        for value in temperature_data:
            update_json("temperature", value)
        humidity_data = request.json["humidity"]
        for value in humidity_data:
            update_json("humidity", value)
    return data

@app.route("/temp")
def temp():
    return render_template("temperature.html")

@app.route("/humidity")
def humidity():
    return render_template("humidity.html")

@app.route("/summary")
def summary():
    accel = get_json("accelerometer")
    temp = get_json("temperature")
    humid = get_json("humidity")
    accel = sorted(accel.values())
    temp = sorted(temp.values())
    humid = sorted(humid.values())
    accel_min, accel_max = accel[1], accel[-1]
    i = 0
    while temp[i] == 0:
        i += 1
    temp_min, temp_max = temp[i], temp[-1]
    j = 0
    while humid[j] == 0:
        j += 1
    humid_min, humid_max = humid[j], humid[-1]

    accel_avg = str(reduce(lambda x, y: x + y, accel)/len(accel))[:5]
    temp_avg = str(reduce(lambda x, y: x + y, temp)/len(temp))[:5]
    humid_avg = str(reduce(lambda x, y: x + y, humid)/len(humid))[:5]

    acc_data = ["Acceleration", accel_min, accel_max, accel_avg]
    temp_data = ["Temperature", temp_min, temp_max, temp_avg]
    humid_data = ["Humidity", humid_min, humid_max, humid_avg]

    final = [acc_data, temp_data, humid_data]

    acc_above_avg = (len([item for item in accel if item >= 0.456]) - 1) * 3 / 60
    acc_below_avg = (len([item for item in accel if item < 0.456]) - 1) * 3 / 60

    temp_above_avg = (len([item for item in temp if item >= 24.10]) - 1) * 3 / 60
    temp_below_avg = (len([item for item in temp if item < 24.10]) - 1) * 3 / 60

    humid_above_avg = (len([item for item in humid if item >= 56.22]) - 1) * 3 / 60
    humid_below_avg = (len([item for item in humid if item < 56.22]) - 1) * 3 / 60

    acc_avg_data = ["Acceleration", acc_above_avg, acc_below_avg]
    temp_avg_data = ["Temperature", temp_above_avg, temp_below_avg]
    humid_avg_data = ["Humidity", humid_above_avg, humid_below_avg]

    averages = [acc_avg_data, temp_avg_data, humid_avg_data]

    acc_score = ["Acceleration", str(100*float(acc_above_avg)/float(len(accel)))[:5]]
    temp_score = ["Temperature", str(100*float(temp_below_avg)/float(len(temp)))[:5]]
    humid_score = ["Humidity", str(100*float(humid_below_avg)/float(len(humid)))[:5]]

    scores = [acc_score, temp_score, humid_score]

    return render_template("summary.html", final=final, averages=averages, scores=scores)

def update_json(field, value):
    data = ""
    script_dir = os.path.dirname(__file__)
    rel_path = "static\\json\\" + field + ".json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "rb") as fp:
        data = json.load(fp)
        fp.close()

    length = len(data)
    data[str(length+1)] = value
    res = collections.OrderedDict(sorted(data.items()))
    jsonFile = open(abs_file_path, "w+")
    jsonFile.write(json.dumps(res))
    jsonFile.close()
    return True

def get_json(field):
    data = ""
    script_dir = os.path.dirname(__file__)
    rel_path = "static\\json\\" + field + ".json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "rb") as fp:
        data = json.load(fp)
        fp.close()
    return data
