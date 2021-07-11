from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user
from sfapp import db
from ..models import User
from ..forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    return render_template('index.html')


@main.route('/completed')
@login_required
def completed():
    if not request.args:
        return render_template('completed.html')

    else:
        search_string = request.args.get('search_string')
        search_value = "%{}%".format(search_string)
        page = request.args.get('page', default=1, type=int)
        return render_template('completed.html', search_string=search_string)


@main.route('/user_register', methods=['GET', 'POST'])
@login_required
def user_register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        email = request.form['email']

        new_user = User(last_name=last_name, first_name=first_name, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.login'))

    return render_template('user_register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('main.index'))

        return 'invalid user name or password'

    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
