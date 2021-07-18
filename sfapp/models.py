from datetime import datetime, timedelta, timezone
from .extentions import db, admin
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView

JST = timezone(timedelta(hours=+9), 'JST')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    action = db.relationship('Action', backref=db.backref('user', lazy=True))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(80), nullable=False)
    group_id = db.Column(db.String(255), db.ForeignKey('lgroup.lgid'), nullable=True)
    message_id = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text(), nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False, default=datetime.now(JST))
    checked = db.Column(db.Integer, nullable=True)
    action = db.relationship('Action', backref='post', uselist=False)


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    checked_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    checked_at = db.Column(db.DateTime, nullable=False, default=datetime.now(JST))
    memo = db.Column(db.String(255), nullable=True)


class Lgroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lgid = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    colour = db.Column(db.String(30), nullable=True)
    post = db.relationship('Post', backref=db.backref('lgroup', lazy=True))


admin.add_view(ModelView(Action, db.session))
admin.add_view(ModelView(Lgroup, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(User, db.session))
