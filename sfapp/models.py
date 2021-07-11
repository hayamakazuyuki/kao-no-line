from .extentions import db, admin
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


admin.add_view(ModelView(User, db.session))
