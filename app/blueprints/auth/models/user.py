from datetime import datetime

from sqlalchemy import func

from app.factories.application import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())

    def __repr__(self):
        return f'<User {self.userame}>'
