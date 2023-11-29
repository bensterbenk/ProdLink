from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login

tag_post_association = Table('tag_post', db.Model.metadata,
                             db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
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


tag_collab_association = Table('tag_collab', db.Model.metadata,
                               db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                               db.Column('collaboration_id', db.Integer, db.ForeignKey('collaboration.id'))
                               )


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    posts = db.relationship("Post", secondary=tag_post_association, back_populates="tags")
    collaborations = db.relationship("Collaboration", secondary=tag_collab_association, back_populates="tags")

    def __repr__(self):
        return '<Tag {}>'.format(self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship("Tag", secondary=tag_post_association, back_populates="posts")

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Collaboration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(255))  # Add a field for file input

    tags = db.relationship('Tag', secondary=tag_collab_association, back_populates='collaborations')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
