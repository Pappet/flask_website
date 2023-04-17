from flask_login import UserMixin
from sqlalchemy.schema import UniqueConstraint
from extensions import db
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(
        db.String(80), unique=True, nullable=False)
    password = db.Column(
        db.String(120), nullable=False)

    # Füge einen benannten UniqueConstraint hinzu
    __table_args__ = (UniqueConstraint('username', name='uq_username'),)

    def get_id(self):
        return str(self.id)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
