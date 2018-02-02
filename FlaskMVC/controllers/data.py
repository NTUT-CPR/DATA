# -*- coding: utf-8 -*-
import base64
import time
import math
import random
import json
import uuid
from datetime import datetime, timedelta

from flask.ext.login import login_required, login_user, logout_user, current_user
from flask import render_template, redirect, url_for, request, make_response, session

from FlaskMVC.service import app, db, csrf, mongo
from FlaskMVC.service import get_blueprint
from FlaskMVC.models.units.tools import getRandomKey, checkUserToken, getUserToken
from FlaskMVC.models.units.opendata import getWeatherData, rootId2Str, getAQIData, getUVData
from FlaskMVC.models.form.CDNForm import CDNForm
from FlaskMVC.models.units.tools import image_upload


app = get_blueprint('index')

session_expiry = 60 * 60 * 6
@app.route('/get_opendata/<int:root_id>', methods=['GET'])
def get_opendata(root_id):
    site_name = rootId2Str(root_id)
    ret = {}
    for _d in getWeatherData():
        if (_d['SiteName'] == site_name):
            ret['weather'] = _d
    for _d in getAQIData():
        if (_d['SiteName'] == site_name):
            ret['aqi'] = _d
    for _d in getUVData():
        if (_d['SiteName'] == site_name):
            ret['uv'] = _d
    return json.dumps(ret, ensure_ascii=False)

@csrf.exempt
@app.route('/set_iotdata/', methods=['POST'])
def set_iotdata():
    data = {
        "root_id": float(request.json['rootId']),
        "node_id": float(request.json['nodeId']),
        "date_time": float(request.json['time']),
        "temperature": float(request.json['temperature'])
    }
    mongo.db.iot.insert_one(data)
    print(data)
    return "seccess"


@app.route('/get_iot/<int:root_id>', methods=['GET'])
def get_iot(root_id):
    print(root_id)
    result = mongo.db.iot.find({"root_id": root_id}).sort([("_id", -1)]).limit(1)
    data = []
    for _d in result:
        data.append({
        "root_id": _d['root_id'],
        "node_id": _d['node_id'],
        "date_time": _d['date_time'],
        "temperature": _d['temperature']
    })

    return json.dumps(data, ensure_ascii=False)

@csrf.exempt
@app.route('/upload_cdn/', methods=['POST'])
def upload_cdn():
    form = CDNForm(csrf_enabled=False)
    if form.validate_on_submit():
        if form.cdn_log_file.data.filename:
            with open(image_upload(form.cdn_log_file.data), 'rb') as fp:
                pass
            
            return 'success'

    return 'error'
