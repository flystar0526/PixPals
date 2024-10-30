import os
import uuid
from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from models import db, Post, Comment, PostLike, PostFavor
from post import post_bp
from utils.forms import PostForm, CommentForm

UPLOAD_FOLDER = 'static/posts'

@post_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        # Image upload handling
        image_filename = None
        if form.image.data:
            image_file = form.image.data
            original_filename = secure_filename(image_file.filename)
            # Use UUID to generate a unique file name, retaining the extension
            unique_filename = f"{uuid.uuid4().hex}{os.path.splitext(original_filename)[1]}"
            image_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, unique_filename)

            # Ensure the upload folder exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            # Save the image
            image_file.save(image_path)
            image_filename = unique_filename

        # Create post
        post = Post(
            title=form.title.data,
            content=form.content.data,
            image=image_filename,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()

        flash('貼文已建立', 'success')
        return redirect(url_for('index'))

    return render_template('post/create_post.html', form=form)

@post_bp.route('/<post_id>', methods=['GET', 'POST'])
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            post_id=post_id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('留言已新增', 'success')
        return redirect(url_for('post.post_detail', post_id=post_id))

    return render_template('post/post_detail.html', post=post, form=form)

@post_bp.route('/like/<post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    like = PostLike.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if like:
        # If already liked, then unlike
        db.session.delete(like)
        db.session.commit()
        return jsonify({'status': 'unliked', 'likes_count': Post.query.get(post_id).likes_count})
    else:
        # Add like
        new_like = PostLike(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify({'status': 'liked', 'likes_count': Post.query.get(post_id).likes_count})

@post_bp.route('/favor/<post_id>', methods=['POST'])
@login_required
def favor_post(post_id):
    favor = PostFavor.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if favor:
        # If already favorited, then unfavorite
        db.session.delete(favor)
        db.session.commit()
        return jsonify({'status': 'unfavorited', 'favorites_count': Post.query.get(post_id).favorites_count})
    else:
        # Add to favorites
        new_favor = PostFavor(user_id=current_user.id, post_id=post_id)
        db.session.add(new_favor)
        db.session.commit()
        return jsonify({'status': 'favorited', 'favorites_count': Post.query.get(post_id).favorites_count})
