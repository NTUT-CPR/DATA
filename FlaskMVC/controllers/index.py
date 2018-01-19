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

from FlaskMVC.service import app, db
from FlaskMVC.service import get_blueprint
from FlaskMVC.models.form.LoginForm import LoginForm
from FlaskMVC.models.db.StreamKey import StreamKey
from FlaskMVC.models.db.Session import Session

app = get_blueprint('index')

@app.route('create_session', methods=['GET'])
def create_session():
    temp = uuid.uuid4().hex
    resp = make_response("DBMS cookies")
    resp.set_cookie("session",temp)

    session = Session(user_id='106598000', session_id=temp, expiry=datetime.today())
    
    db.session.add_all([session])
    db.session.commit()
    return 'seccess'

@app.route('create_key', methods=['GET'])
def create_key(): 
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
    print(id)
    key = StreamKey.query.filter_by(id=id).first()
    bdata = bytearray(b'\x00\x00\x00\x01')
    bdata += base64.b64decode(key.key_id)
    bdata += bytearray(b'\x00\x00\x00\x00')
    data = base64.b64encode(bdata).decode('ascii')
    return json.dumps([{"key":key.key,"key_id":key.key_id,"pssh":[{"uuid":"1077efec-c0b2-4d02-ace3-3c1e52e2fb4b","data":data}]}])



@app.route('get_key2/<id>', methods=['GET'])
def get_key2(id):
    print(id)
    key = StreamKey.query.filter_by(id=5).first()
    bdata = bytearray(b'\x00\x00\x00\x01')
    bdata += base64.b64decode(key.key_id)
    bdata += bytearray(b'\x00\x00\x00\x00')
    data = base64.b64encode(bdata).decode('ascii')
    return json.dumps([{"key":key.key,"key_id":key.key_id,"pssh":[{"uuid":"1077efec-c0b2-4d02-ace3-3c1e52e2fb4b","data":data}]}])



@app.route('lis/', methods=['GET'])
def lis():
    return json.dumps({"keys": [{"k": "YzJmODYxNzM3Y2M0ZjM4Mg", "kty": "oct", "kid": "GzoNU9Dfwc//Iq3/zbzMUw" }], "type": "temporary"})


def getRandomKey():
    return bytes.decode(base64.b64encode(str.encode(''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+', 16)))))
