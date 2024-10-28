from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

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
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    image = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.String, db.ForeignKey('posts.id'), nullable=False)
    content = db.Column(db.String, nullable=False)

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
