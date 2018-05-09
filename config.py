from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from hashlib import sha256

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pouriya:haval@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)


class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    # segment = db.relationship('Segment', backref='user', lazy=True)
    # slot = db.relationship('Slot', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r, %s>' % (self.username, self.password)


class Slot(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80))

    _date = db.Column(db.DateTime)
    _author = db.Column(db.Integer, db.ForeignKey('user._id'))

    # segment = db.relationship('Segment', backref='slot', lazy=True)

    def __init__(self, code, user_id):
        self.code = code
        self._author = user_id

    def __repr__(self):
        return '<Code %r>' % self.code


class Segment(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.DateTime)
    tail = db.Column(db.DateTime)
    slot = db.Column(db.Integer, db.ForeignKey('slot._id'))

    _date = db.Column(db.DateTime)
    _author = db.Column(db.Integer, db.ForeignKey('user._id'))

    def __init__(self, slot, head, tail, user_id):
        self.slot = slot
        self.head = head
        self.tail = tail
        self.date = datetime.now()
        self._author = user_id

    def __repr__(self):
        return '<[head tail) %r>' % self.head, self.tail


admin = User('admin', 'admin@example.com', sha256('admin'.encode()).hexdigest())
# #
db.drop_all()
db.create_all() # In case user table doesn't exists already. Else remove it.
# #
db.session.add(admin)
# #
db.session.commit() # This is needed to write the changes to database
#
# # User.query.delete()
# print(User.query.all())
#

# print(User.query.filter_by(username='admin').first()._id)
