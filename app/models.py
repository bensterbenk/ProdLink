
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login

artist_event_association = Table('artist_event', db.Model.metadata,
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    genre = db.Column(db.String(64))
    bio = db.Column(db.String(64))
    events = db.relationship("Event", secondary=artist_event_association, back_populates="artists")
    def __repr__(self):
        return '<User {}>'.format(self.name)


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200))
    def __repr__(self):
        return '<User {}>'.format(self.name)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    time = db.Column(db.Date, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artists = db.relationship("Artist", secondary=artist_event_association, back_populates="events")
    def __repr__(self):
        return '<User {}>'.format(self.name)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))