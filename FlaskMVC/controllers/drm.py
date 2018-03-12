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

from FlaskMVC.service import app, db, csrf
from FlaskMVC.service import get_blueprint
from FlaskMVC.models.db.StreamKey import StreamKey
from FlaskMVC.models.db.Session import Session
from FlaskMVC.models.units.tools import getRandomKey, checkUserToken, getUserToken


app = get_blueprint('index')
dash = get_blueprint('dash')

session_expiry = 60 * 60 * 6

@app.route('/create_session', methods=['GET'])
def create_session():
    """
    新增Session
    """
    user_id = int(request.args.get('user_id', '-1'))
    token = request.args.get('token', '')
    if checkUserToken(user_id, token) is False:
        return json.dumps({'message':'token_error'})

    if 'session' in request.cookies:
        session = Session.query.filter_by(user_id=user_id, session_id=request.cookies['session']).first()
        if session is not None and session.expiry > datetime.today():
            return json.dumps({'message':'session_exist'})

    expiry = datetime.today() +  timedelta(hours=6)
    session_id = uuid.uuid4().hex
    resp = make_response(json.dumps({'message':'success'}))
    resp.set_cookie("session", session_id, expiry.timestamp())

    session = Session(user_id=user_id, session_id=session_id, expiry=expiry)
    
    db.session.add(session)
    db.session.commit()
    return resp

@app.route('/create_key/<int:stream_id>', methods=['GET'])
def create_key(stream_id): 
    """
    建立串流KEY
    """
    #檢查Session內容
    if 'session' not in request.cookies:
        return json.dumps({'message':'not logined.'}), 403

    session = Session.query.filter_by(session_id=request.cookies['session']).first()
    if session is None or session.expiry <= datetime.today():
        return json.dumps({'message':'not logined.'}), 403

    #輸入參數消毒
    if stream_id < 1:
        return json.dumps({'message':'stream id incorrect.'}), 406

    #檢查是否已經產生過stream key
    stream_key = StreamKey.query.filter_by(session_id=session.session_id, stream_id=stream_id).first()
    if stream_key is not None:
        return json.dumps({
        "stream_key_id": stream_key.stream_key_id,
        "key":stream_key.key,
        "key_id":stream_key.key_id})

    #產生stream key
    key_id = getRandomKey()
    key = getRandomKey()
    stream_key = StreamKey(key_id=key_id, key=key, session_id=session.session_id, stream_id=stream_id)
    db.session.add(stream_key)
    db.session.commit()
    return json.dumps({
        "stream_key_id": stream_key.stream_key_id,
        "key":stream_key.key,
        "key_id":stream_key.key_id})


@app.route('/get_key/<int:stream_id>/<int:stream_key_id>', methods=['GET'])
def get_key(stream_id, stream_key_id):
    """
    給VOD MODULE串流KEY
    id: KEY的ID
    """
    key = StreamKey.query.filter_by(stream_key_id=stream_key_id).first()
    if key is None or key.session.expiry <= datetime.today():
        return json.dumps({'message':'key error.'}), 403

    bdata = bytearray(b'\x00\x00\x00\x01')
    bdata += base64.b64decode(key.key_id)
    bdata += bytearray(b'\x00\x00\x00\x00')
    data = base64.b64encode(bdata).decode('ascii')
    return json.dumps([{"key":key.key, "key_id":key.key_id, "pssh":[{"uuid":"1077efec-c0b2-4d02-ace3-3c1e52e2fb4b", "data":data}]}])


@dash.route('/<int:stream_id>/<int:stream_key_id>', methods=['GET'])
def get_path(stream_id, stream_key_id):
    """
    給VOD MODULE串流KEY
    id: KEY的ID
    """
    key = StreamKey.query.filter_by(stream_key_id=stream_key_id, stream_id=stream_id).first()
    if key is None or key.session.expiry <= datetime.today():
        return json.dumps({'message':'key error.'}), 403

    if stream_id  == 1:
        return json.dumps({"sequences": [{"clips": [{"type": "source","path": "/opt/static/videos/str.mp4"}]}]}) 
    if stream_id  == 2:
        return json.dumps({"sequences": [{"clips": [{"type": "source","path": "/opt/static/videos/video3.mp4"}]}]}) 
    if stream_id  == 3:
        return json.dumps({"sequences": [{"clips": [{"type": "source","path": "/opt/static/videos/sakura.mp4"}]}]}) 
    if stream_id == 4:
        return json.dumps({"sequences": [{"clips": [{"type": "source","path": "/opt/static/videos/qp22_elephants_dream_1080p24.mp4"}]}]}) 

    return json.dumps({'message':'stream not exist.'}), 404


@app.route('/dash/<int:stream_id>/<int:stream_key_id>', methods=['GET'])
def get_path2(stream_id, stream_key_id):
    """
    給VOD MODULE串流KEY
    id: KEY的ID
    """
    key = StreamKey.query.filter_by(stream_key_id=stream_key_id, stream_id=stream_id).first()
    if key is None or key.session.expiry <= datetime.today():
        return json.dumps({'message':'key error.'}), 403

    if stream_id  == 1:
        return json.dumps({"sequences": [{"clips": [{"type": "source","path": "/opt/static/videos/str.mp4"}]}]}) 
    if stream_id  == 2:
        return json.dumps({"sequences": [{"clips": [{"type": "source","path": "/opt/static/videos/video3.mp4"}]}]}) 
    if stream_id  == 3:
        return json.dumps({"sequences": [{"clips": [{"type": "source","path": "/opt/static/videos/sakura.mp4"}]}]}) 
    if stream_id == 4:
        return json.dumps({"sequences": [{"clips": [{"type": "source","path": "/opt/static/videos/qp22_elephants_dream_1080p24.mp4"}]}]}) 

    return json.dumps({'message':'stream not exist.'}), 404
