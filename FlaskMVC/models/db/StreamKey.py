from FlaskMVC.service import db


class StreamKey(db.Model):
    __tablename__ = "stream_keys"
    id = db.Column(db.Integer, primary_key=True)
    key_id = db.Column(db.String(32))
    key = db.Column(db.String(32))
    session_id = db.Column(db.String(32))
    stream_id = db.Column(db.Integer)
