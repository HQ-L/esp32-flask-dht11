from ast import If
from crypt import methods
from email.mime import base
from json.tool import main
from pydoc import render_doc
from unicodedata import name
from application import app
from flask import redirect, render_template, request, url_for
import requests
import json

flag = {"flag":0}
ret_th = {"温度":0, "湿度":0}
@app.route("/", methods=['GET', 'POST'])
@app.route("/control", methods=['GET', 'POST'])
def control():
    if request.method == 'GET':
        return render_template("control.html", data_ret_th=ret_th)
    if request.method == 'POST':
        ret = request.form.get('data_flag')
        if ret == '1':
            re = 1
        elif ret == '2':
            re = 2
        else:
            re = 0
        global flag
        flag = {"flag":re}
        # print(flag)
        return render_template("control.html", data_ret_th=ret_th)

@app.route("/getFlag", methods=['GET', 'POST'])
def getFlag():
    # print(flag)
     return flag

@app.route("/setFlag", methods=['GET', 'POST'])
def setFlag():
    global flag
    flag = {"flag":request.args.get("flag")}
    return flag

@app.route("/getdht11_lts", methods=['GET', 'POST'])
def getdht11_lts():
    t = request.args.get("t")
    h = request.args.get("h")
    global ret_th
    ret_th = {"温度":t, "湿度":h}
    return ret_th


@app.route("/getdht11", methods=['GET', 'POST'])
def getdht11():
    if request.method == 'POST':
        t = request.json.get("t")
        h = request.json.get("h")
        global ret_th
        ret_th = {"temp":t, "humi":h}
    if request.method == 'GET':
        return ret_th


# @app.route("/showdht11", methods=['GET', 'POST'])
# def showdht11():
#     return render_template("control.html", ret_th)
