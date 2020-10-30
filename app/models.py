import json
import ast
import datetime
from . import db
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base

class Json(db.TypeDecorator):

    impl = db.String

    def process_bind_param(self, value, dialect):
        return json.dumps(str(value))

    def process_result_value(self, value, dialect):
        return ast.literal_eval(json.loads(value))


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    embeeding = db.Column(Json(2000))
    link= db.Column(db.String(300))

class ShopLists(db.Model):
    id_product = db.Column(db.Integer, primary_key=True)
    id_user=db.Column(db.Integer)
    content = db.Column(db.Text)

    def __init__(self, id_user, content):
    	self.id_user = id_user
    	self.content = content

    def __repr__(self):
        return '<Content %s>' % self.content

class Status(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	id_user=db.Column(db.Integer)
	status = db.Column(db.String(50))
	date_created=db.Column(db.DateTime, default=datetime.datetime.utcnow())

	def __init__(self, id_user, status,date_created):
		self.id_user = id_user
		self.status = status
		self.date_created = date_created