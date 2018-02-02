from FlaskMVC.service import db


class StreamKey(db.Model):
    __tablename__ = "stream_keys"
    stream_key_id = db.Column(db.Integer, primary_key=True)
    key_id = db.Column(db.String(32))
    key = db.Column(db.String(32))
    session_id = db.Column(db.String(32), db.ForeignKey("sessions.session_id"))
    stream_id = db.Column(db.Integer)
    session = db.relationship('Session', backref='stream_keys')

    def __repr__(self):
        return '<StreamKey %r>' % self.id
