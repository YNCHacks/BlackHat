from app import app
from flask import render_template, flash, redirect, url_for, request, Response
import json
import os
import collections

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
