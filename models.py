from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)  # +79123456789
    username = db.Column(db.String(80), unique=True)  # опционально
    tournaments = db.relationship('Tournament', backref='owner', lazy=True)
