import os
import uuid
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from models import db, User
from utils.forms import RegisterForm, LoginForm
from auth import auth_bp

UPLOAD_FOLDER = 'static/avatars'


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            flash('Email 已被註冊', 'danger')
            return redirect(url_for('auth.register'))

        # Handle avatar upload
        avatar_filename = None
        if form.avatar.data:
            avatar_file = form.avatar.data
            original_filename = secure_filename(avatar_file.filename)
            # Generate a unique filename using UUID, preserving the original extension
            unique_filename = f"{uuid.uuid4().hex}{os.path.splitext(original_filename)[1]}"
            avatar_path = os.path.join(UPLOAD_FOLDER, unique_filename)

            # Ensure the upload folder exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            # Save avatar
            avatar_file.save(avatar_path)
            avatar_filename = unique_filename

        # Create a new user
        user = User(name=name, email=email, avatar=avatar_filename)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('註冊成功，請登入', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('登入成功', 'success')
            return redirect(url_for('index'))
        flash('無效的 email 或密碼', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已登出', 'info')
    return redirect(url_for('auth.login'))
