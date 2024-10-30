import os
import uuid
from flask import render_template, redirect, url_for, flash, request, current_app, session
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from models import db, Post, PostLike, PostFavor
from user import user_bp
from utils.forms import EditProfileForm

UPLOAD_FOLDER = 'static/avatars'

@user_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    # Save the previous page URL into the session
    if request.method == 'GET':
        session['previous_url'] = request.referrer or url_for('index')

        # Pre-fill the form with default data
        form.email.data = current_user.email
        form.name.data = current_user.name

    if form.validate_on_submit():
        # Update user information
        current_user.name = form.name.data

        if form.password.data:
            current_user.set_password(form.password.data)

        # Handle avatar upload
        if form.avatar.data:
            avatar_file = form.avatar.data
            original_filename = secure_filename(avatar_file.filename)
            # Generate a unique filename using UUID and retain the file extension
            unique_filename = f"{uuid.uuid4().hex}{os.path.splitext(original_filename)[1]}"
            avatar_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, unique_filename)

            # Ensure the upload folder exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            # Save the new avatar
            avatar_file.save(avatar_path)

            # Delete the old avatar (if not the default avatar)
            if current_user.avatar and current_user.avatar != 'default-avatar.png':
                old_avatar_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, current_user.avatar)
                if os.path.exists(old_avatar_path):
                    os.remove(old_avatar_path)

            # Update the avatar name in the database
            current_user.avatar = unique_filename

        # Commit the changes
        db.session.commit()
        flash('個人資料已更新', 'success')

        # Retrieve the previous page URL from the session and redirect
        previous_url = session.get('previous_url', url_for('index'))
        return redirect(previous_url)

    return render_template('user/edit_profile.html', form=form)

@user_bp.route('/profile')
@login_required
def profile():
    # User's published posts
    posts = Post.query.filter_by(user_id=current_user.id).all()

    # User's liked posts
    liked_posts = Post.query.join(PostLike, Post.id == PostLike.post_id) \
                            .filter(PostLike.user_id == current_user.id).all()

    # User's favorited posts
    favorited_posts = Post.query.join(PostFavor, Post.id == PostFavor.post_id) \
                                .filter(PostFavor.user_id == current_user.id).all()

    return render_template(
        'user/profile.html', 
        user=current_user, 
        posts=posts, 
        liked_posts=liked_posts, 
        favorited_posts=favorited_posts
    )
