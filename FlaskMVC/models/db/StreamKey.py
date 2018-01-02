from FlaskMVC.service import db


class StreamKey(db.Model):
    __tablename__ = "stream_keys"
    key_id = db.Column(db.String(32), primary_key=True)
    key = db.Column(db.String(32))
    session_id = db.Column(db.String(32))
    stream_id = db.Column(db.Integer)
