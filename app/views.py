from app import app
from flask import render_template, flash, redirect, url_for, request, Response
import json
import os

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        accelerometer_data = request.json["accelerometer"]
        temperature_data = request.json["temperature"]
        dust_data = request.json["dust"]
        humidity_data = request.json["humidity"]
    return
