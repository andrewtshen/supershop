from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __bind_key__ = "user"
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    favorite_drink = db.Column(db.String(1000), unique=False, default="")
    is_set_favorite_drink = db.Column(db.Boolean, unique=False, default=False)

class User_Group(db.Model):
    __bind_key__ = "user_group"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=False)
    group_id = db.Column(db.Integer, unique=False)

class Group(db.Model):
    __bind_key__ = "group"
    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)

