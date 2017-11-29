from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    """
    登入表單
    """

    name = StringField(validators=[DataRequired(message="請輸入你的帳號。")])
    password = PasswordField(validators=[DataRequired(message="請輸入你的密碼。")])
