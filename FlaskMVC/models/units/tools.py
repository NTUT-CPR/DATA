import hashlib
import string
import os
import json
import random

from werkzeug.utils import secure_filename
from FlaskMVC.service import app
from flask import flash

SIMPLE_CHARS = string.ascii_letters + string.digits
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/../../static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_random_string(length = 24):
    """
    產生一組亂數字串
    :param length: 亂數字串長度，預設24
    :return: 亂數字串
    """
    ret_str = ''
    while length > 0:
        ret_str = ret_str.join(random.choice(SIMPLE_CHARS))
        length -= 1
    return ret_str


def password_encryption(password):
    """
    將密碼用sha256加密
    :param password: 密碼明碼
    :return: 雜湊後的密碼
    """
    return hashlib.sha256(password.encode('ascii')).hexdigest()


def allowed_file(filename):
    """
    過濾副檔名
    :param filename: 表單回傳的檔案物件
    :return: 布林值，副檔名是否合法
    """
    allow_extensions = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allow_extensions


def image_upload(file):
    """
    上傳檔案
    :param file: 表單回傳的檔案物件
    :return: 布林值，成功與否
    """
    if file and allowed_file(file.filename):
        filename = get_random_string() + secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    return None


def delete_image(filename):
    """
    刪除檔案
    :param filename: 要刪除的檔案名稱
    :return: 布林值，成功與否
    """
    if allowed_file(filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(filename):
            os.remove(filename)
        return True
    return None


def required_to_flash(form):
    """
    將 wtf 產生的 required 改成 flash 方式送給templates
    :param form: 表單物件
    :return: 無
    """
    for name, messages in form.errors.items():
        for message in messages:
            flash(message)


def jqgrid_json(success, message=''):
    """
    回傳給jqgrid的json格式
    :param success: 布林值，是否成功
    :param message: 失敗時的訊息
    :return: json字串
    """
    src = {
        "success":  success,
        "message":  message
    }
    return json.dumps(src)
