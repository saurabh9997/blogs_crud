from datetime import datetime

from sqlalchemy import func

from app.factories.application import db


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())

    def __repr__(self):
        return f'<BlogPost {self.title}>'
