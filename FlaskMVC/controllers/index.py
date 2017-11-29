# -*- coding: utf-8 -*-
import time
import math
import random
import json
from datetime import datetime, timedelta

from flask.ext.login import login_required, login_user, logout_user, current_user
from flask import render_template, redirect, url_for, request, session

from FlaskMVC.service import get_blueprint
from FlaskMVC.models.form.LoginForm import LoginForm

index = get_blueprint('index')

@index.route('/', methods=['GET'])
def index():

    return "[{\"key\":\"FRYXGBkaGxwdHh8gISIjJA==\",\"key_id\":\"ICEiIyQlJicoKSorLC0uLw==\",\"pssh\":[{\"uuid\":\"1077efec-c0b2-4d02-ace3-3c1e52e2fb4b\",\"data\":\"AAAAASAhIiMkJSYnKCkqKywtLi8AAAAA\"}]}]"


