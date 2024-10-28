import os
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

    # 保存上一頁的 URL 進入 session
    if request.method == 'GET':
        session['previous_url'] = request.referrer or url_for('index')

        # 預設填充表單資料
        form.email.data = current_user.email
        form.name.data = current_user.name

    if form.validate_on_submit():
        # 更新用戶資料
        current_user.name = form.name.data

        if form.password.data:
            current_user.set_password(form.password.data)

        # 處理頭像上傳
        if form.avatar.data:
            avatar_file = form.avatar.data
            filename = secure_filename(avatar_file.filename)
            avatar_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, filename)
            avatar_file.save(avatar_path)
            current_user.avatar = filename

        # 提交變更
        db.session.commit()
        flash('個人資料已更新', 'success')

        # 從 session 中取出上一頁的 URL 並跳轉
        previous_url = session.get('previous_url', url_for('index'))
        return redirect(previous_url)

    return render_template('user/edit_profile.html', form=form)

@user_bp.route('/profile')
@login_required
def profile():
    # 使用者的發布貼文
    posts = Post.query.filter_by(user_id=current_user.id).all()

    # 使用者按讚過的貼文
    liked_posts = Post.query.join(PostLike, Post.id == PostLike.post_id) \
                            .filter(PostLike.user_id == current_user.id).all()

    # 使用者收藏過的貼文
    favorited_posts = Post.query.join(PostFavor, Post.id == PostFavor.post_id) \
                                .filter(PostFavor.user_id == current_user.id).all()

    return render_template(
        'user/profile.html', 
        user=current_user, 
        posts=posts, 
        liked_posts=liked_posts, 
        favorited_posts=favorited_posts
    )
