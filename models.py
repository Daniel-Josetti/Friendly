from db import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), unique=True, nullable=False)
    senha = db.Column(db.String(), nullable=False)
    cargo = db.Column(db.String(), default='student')