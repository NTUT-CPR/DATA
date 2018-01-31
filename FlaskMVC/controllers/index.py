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
from FlaskMVC.models.form.LoginForm import LoginForm
from FlaskMVC.models.db.StreamKey import StreamKey
from FlaskMVC.models.db.Session import Session
from FlaskMVC.models.units.tools import getRandomKey, getCWBData, rootId2Str

app = get_blueprint('index')

@app.route('create_session', methods=['GET'])
def create_session():
    """
    新增Session
    """
    temp = uuid.uuid4().hex
    resp = make_response("DBMS cookies")
    resp.set_cookie("session",temp)

    session = Session(user_id='106598000', session_id=temp, expiry=datetime.today())
    
    db.session.add_all([session])
    db.session.commit()
    return 'seccess'

@app.route('create_key', methods=['GET'])
def create_key(): 
    """
    建立串流KEY
    """
    key_id = getRandomKey()
    key = getRandomKey()
    key = StreamKey(key_id=key_id, key=key, session_id='3a52187e19964e718cc9ef0fe93ff71f', stream_id=1)
    db.session.add_all([key])
    db.session.commit()
    return json.dumps([{
        "id": key.id,
        "key":key.key,
        "key_id":key.key_id}])


@app.route('get_key/<id>', methods=['GET'])
def get_key(id):
    """
    給VOD MODULE串流KEY
    id: KEY的ID
    """
    key = StreamKey.query.filter_by(id=id).first()
    bdata = bytearray(b'\x00\x00\x00\x01')
    bdata += base64.b64decode(key.key_id)
    bdata += bytearray(b'\x00\x00\x00\x00')
    data = base64.b64encode(bdata).decode('ascii')
    return json.dumps([{"key":key.key, "key_id":key.key_id, "pssh":[{"uuid":"1077efec-c0b2-4d02-ace3-3c1e52e2fb4b", "data":data}]}])


@app.route('dash/<id>/<video>', methods=['GET'])
def dash(id, video):
    """
    給VOD MODULE串流KEY
    id: KEY的ID
    """
    print(video)
    return json.dumps({"sequences": [{"clips": [{"type": "source","path": "/opt/static/videos/"+video}]}]}) 


@app.route('get_key2/<id>', methods=['GET'])
def get_key2(id):
    print(id)
    key = StreamKey.query.filter_by(id=5).first()
    bdata = bytearray(b'\x00\x00\x00\x01')
    bdata += base64.b64decode(key.key_id)
    bdata += bytearray(b'\x00\x00\x00\x00')
    data = base64.b64encode(bdata).decode('ascii')
    return json.dumps([{"key":key.key,"key_id":key.key_id,"pssh":[{"uuid":"1077efec-c0b2-4d02-ace3-3c1e52e2fb4b","data":data}]}])

@app.route('get_cwbdata/<int:root_id>', methods=['GET'])
def get_cwbdata(root_id):
    site_name = rootId2Str(root_id)
    for _d in getCWBData():
        if (_d['SiteName'] == site_name):
            return json.dumps(_d, ensure_ascii=False)
    return {}

@csrf.exempt
@app.route('set_iotdata/', methods=['POST'])
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


@app.route('get_iot/<int:root_id>', methods=['GET'])
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
