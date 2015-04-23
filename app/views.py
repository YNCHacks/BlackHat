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
    data = "hello"
    """
    if request.method == "POST":
        accelerometer_data = request.json["Acceleration"]
        data = accelerometer_data
    """
    return data
