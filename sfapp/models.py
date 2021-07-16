from datetime import datetime
from .extentions import db, admin
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(80), nullable=False)
    group_id = db.Column(db.String(255), nullable=True)
    message_id = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text(), nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    checked = db.Column(db.Integer, nullable=True)


"""class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    checked_by = db.Column(db.Integer, nullable=False)
    checked_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    memo = db.Column(db.String, nullable=True)
"""

admin.add_view(ModelView(User, db.session))
