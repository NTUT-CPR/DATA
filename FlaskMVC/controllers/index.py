# -*- coding: utf-8 -*-
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
    key = StreamKey(key_id=uuid.uuid4().hex, key=uuid.uuid4().hex, session_id='3a52187e19964e718cc9ef0fe93ff71f', stream_id=1)
    db.session.add_all([key])
    db.session.commit()
    return 'seccess'

@app.route('get_key', methods=['GET'])
def get_key():
    key = StreamKey.query.filter_by(key_id='f4ef71d2e83541a7a4529616dba9e831').first()

    return json.dumps([{"key":key.key,"key_id":key.key_id,"pssh":[{"uuid":"1077efec-c0b2-4d02-ace3-3c1e52e2fb4b","data":"AAAAASAhIiMkJSYnKCkqKywtLi8AAAAA"}]}])




