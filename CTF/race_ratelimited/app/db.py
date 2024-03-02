from . import app
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha3_256, sha3_512
from .config import DB_URI, HASH_ROUNDS

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.relationship('User', backref=db.backref('messages', lazy=True))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    img = db.Column(db.String(120), unique=False, nullable=True)
    content = db.Column(db.Text, unique=False, nullable=True)
    time = db.Column(db.Integer, unique=False, nullable=False)
    likes = db.relationship('Like', back_populates='message', lazy=True)
    
    def __hash__(self) -> int:
        data = self.sender.username.encode() + self.img.encode() + self.content.encode()
        for _ in range(HASH_ROUNDS):
            data = sha3_512(data).digest()
        return int.from_bytes(data, "big")

    def __eq__(self, o: object) -> bool:
        return self.__hash__() == o.__hash__()
    
    def __repr__(self):
        return '<Message %r>' % (self.content)

class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', backref=db.backref('likes', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.relationship('Message', back_populates='likes', lazy=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    date = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Like %r>' % (self.id)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    got_tons_like = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    def __repr__(self):
        return '<User %r, items:%d>' % (self.username, len(self.items))

    def verify_password(self, password):
        h = sha3_256(password.encode('utf-8')).hexdigest()
        if h == self.password:
            return True
        return False

    def set_password(self, password):
        h = sha3_256(password.encode('utf-8')).hexdigest()
        self.password = h



