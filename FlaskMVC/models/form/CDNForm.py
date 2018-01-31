from flask.ext.wtf import Form

from wtforms import FileField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class CDNForm(Form):
    """
    CDN上傳表單
    """
    cdn_log_file = FileField(validators=[DataRequired(message="請選擇上傳音檔")])
