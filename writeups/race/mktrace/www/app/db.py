from . import app
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha3_256
from config import DB_URI

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    coins = db.Column(db.Integer, unique=False, nullable=False, default=0)
    euro = db.Column(db.Integer, unique=False, nullable=False, default=100)
    mkt_id = db.Column(db.Integer, db.ForeignKey('market.id'), nullable=True)
    market = db.relationship('Market', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User %r %.2f🪙 %.2f€>' % (self.username, self.coins/100, self.euro/100)

    def verify_password(self, password):
        h = sha3_256(password.encode('utf-8')).hexdigest()
        if h == self.password:
            return True
        return False

    def set_password(self, password):
        h = sha3_256(password.encode('utf-8')).hexdigest()
        self.password = h


class Market(db.Model):
    __tablename__ = 'market'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    date = db.Column(db.DateTime(), unique=False, nullable=False)

    def __repr__(self):
        return '<Market %r [%d] >' % (self.name, len(self.orders))

    def verify_password(self, password):
        h = sha3_256(password.encode('utf-8')).hexdigest()
        if h == self.password:
            return True
        return False

    def set_password(self, password):
        h = sha3_256(password.encode('utf-8')).hexdigest()
        self.password = h

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    coins = db.Column(db.Integer, unique=False, nullable=False)
    euro = db.Column(db.Integer, unique=False, nullable=False)
    is_buy = db.Column(db.Boolean(), unique=False, nullable=False, default=False)
    date = db.Column(db.DateTime(), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    mkt_id = db.Column(db.Integer, db.ForeignKey('market.id'), nullable=False)
    market = db.relationship('Market', backref=db.backref('orders', lazy=True))


    def __repr__(self):
        return '<Order [%r] %s %d🪙 %.2f€ %r>' % (self.id, "buy" if self.is_buy else "sell", self.coins, self.euro/100, self.date)

