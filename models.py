from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __bind_key__ = "user"
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    firstName = db.Column(db.String(1000))
    lastName = db.Column(db.String(1000))


