from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, app
from flask_login import UserMixin
from app import login
from flask import current_app
import os
from werkzeug.utils import secure_filename

tag_post_association = Table('tag_post', db.Model.metadata,
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)
comment_post_association = Table('comment_post', db.Model.metadata,
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    posts = db.relationship("Post", secondary=tag_post_association, back_populates="tags")
    tag_type = db.Column(db.String(64), index=True)
    def __repr__(self):
        return '<Tag {}>'.format(self.name)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    audio_file = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship("Tag", secondary=tag_post_association, back_populates="posts")
    comments = db.relationship("Comment", secondary=comment_post_association, back_populates="posts")
    def save_audio(self, audio_file):
        if audio_file:
            audio_filename = secure_filename(audio_file.filename)
            audio_folder = os.path.join(app.root_path, 'static/audio')


            # Ensure the destination directory exists
            os.makedirs(audio_folder, exist_ok=True)

            audio_path = os.path.join(audio_folder, audio_filename)
            audio_file.save(audio_path)
            self.audio_file = audio_filename
            db.session.commit()
    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posts = db.relationship("Post", secondary=comment_post_association, back_populates="comments")
    def __repr__(self):
        return '<Comment {}>'.format(self.body)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

