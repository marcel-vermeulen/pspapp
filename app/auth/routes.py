from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from datetime import datetime

from app import bcrypt, db
from app.auth.forms import LoginForm, RegisterForm, SendResetPasswordRequestForm, ResetPasswordForm
from app.auth.email import send_password_reset_email
from app.model import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        username = username.upper()
        lastlogon = datetime.now()
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        if bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            user.lastlogon = datetime.now()
            db.session.add(user)
            db.session.commit()            
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Password incorrect', category='danger')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('You are now logged out.', category='info')
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        email=form.email.data
        ipam=form.password.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=username.upper(), email=email.lower(), password=hashed_password,firstname=form.firstname.data,surname=form.surname.data,mobile=form.mobile.data,ipam=ipam)
        #password = bcrypt.generate_password_hash(form.password.data)
        #email = form.email.data
        #user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, register success. You can log in now.', category='info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/send_reset_password_request', methods=['GET', 'POST'])
def send_reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = SendResetPasswordRequestForm(request.form)
    if form.validate_on_submit():
        email=form.email.data
        user = User.query.filter_by(email=email.lower()).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/send_reset_password_request.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm(request.form)
    if form.validate_on_submit():
        user = User.verify_reset_password_token(token)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        #user.password = bcrypt.generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

