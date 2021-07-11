from flask import Blueprint, render_template, request, redirect, url_for

from sfapp import db
from ..models import User
from ..forms import RegisterForm, LoginForm

user = Blueprint('user', __name__)


@user.route('/user_register', methods=['GET', 'POST'])
def user_register():
    form = RegisterForm()
    if form.validate_on_submit():
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(last_name=last_name, first_name=first_name, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('user.login'))

    return render_template('user_register.html', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                return redirect(url_for('main.index'))

        return 'invalid user name or password'

    return render_template('login.html', form=form)
