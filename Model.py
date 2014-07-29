__author__ = 'lixiao187'
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import unittest
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/test.db' % os.path.dirname(__file__)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    devices = db.relationship('Device', backref='user',
                                lazy='dynamic')
    def __init__(self, username, email,passwd):
        self.username = username
        self.email = email
        self.password = passwd

    def __repr__(self):
        return '<User %r>' % self.username
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.Integer)
    name = db.Column(db.String(80), unique=True)
    tags = db.Column(db.String(80))
    description = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sensors = db.relationship('Sensor', backref='device',
                                lazy='dynamic')
    def __init__(self,name,uid,tag,description):
        self.name = name
        self.user_id = uid
        self.tags = tag
        self.description = description
    def __repr__(self):
        return '<Device %r>' % self.name

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.Integer)
    name = db.Column(db.String(80), unique=True)
    tags = db.Column(db.String(80))
    description = db.Column(db.String(512))
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    status=db.Column(db.Integer)

    def __init__(self,name,did,tags,description,status):
        self.name = name
        self.device_id = did
        self.tags = tags
        self.description = description
        self.status = status
    def __repr__(self):
        return '<Sensor %r>' % self.name


class TestSequenceFunctions(unittest.TestCase):
    def test_shuffle(self):
        me = User('admin', 'admin@example.com','285523')
        db.session.add(me)
        db.session.commit()
    def test_addDevice(self):
        #Device
        user = User.query.filter_by(username='admin').first()
        dev = Device(name="hello",uid=user.id)
        db.session.add(dev)
        db.session.commit()
    def test_addSensor(self):
        d = Device.query.filter_by(name='hello').first()
        s = Sensor(name="led",did=d.id)
        db.session.add(s)
        db.session.commit()
    def test_getDevice(self):
        dev = Device.query.get(1);
        print dev

# from Model import User,Device,Sensor,db