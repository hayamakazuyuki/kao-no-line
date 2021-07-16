from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from datetime import datetime
from sfapp import db
from ..models import User, Post
from ..forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    tasks = Post.query.filter_by(checked=None).order_by(Post.id.desc()).paginate(page=page, per_page=20)
    today = datetime.today()
    strtoday = today.strftime('%Y-%m-%d')

    return render_template('index.html', tasks=tasks, strtoday=strtoday)


@main.route('/completed')
@login_required
def completed():
    page = request.args.get('page', 1, type=int)
    checked_tasks = Post.query.filter_by(checked=1).order_by(Post.id.desc()).paginate(page=page, per_page=20)

    return render_template('completed.html', tasks=checked_tasks, page=page)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post_detail(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        post.checked = request.form['checked']
        db.session.commit()

        flash('投稿を確認済みにしました。', 'success')
        return redirect(url_for('main.index'))

    return render_template('post_detail.html', post=post)


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
