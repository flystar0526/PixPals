from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

def generate_uuid():
    return str(uuid4())

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=True)
    image = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='posts', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @property
    def likes_count(self):
        """計算貼文的按讚數量"""
        return PostLike.query.filter_by(post_id=self.id).count()

    @property
    def favorites_count(self):
        """計算貼文的收藏數量"""
        return PostFavor.query.filter_by(post_id=self.id).count()

    @property
    def comments_count(self):
        """計算留言數量"""
        return self.comments.count()

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='comments')

class PostLike(db.Model):
    __tablename__ = 'posts_like'
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.String, db.ForeignKey('posts.id'), nullable=False)

class PostFavor(db.Model):
    __tablename__ = 'posts_favor'
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.String, db.ForeignKey('posts.id'), nullable=False)
