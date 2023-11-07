import datetime
from datetime import datetime
from datetime import date
from flask import Blueprint, render_template, flash, redirect, request, url_for
from .forms import ArtistForm, LoginForm, RegistrationForm, VenueForm, EventForm, EmptyForm
from app import app, models
from app.models import Artist, Venue, Event
from app import db
from flask_login import current_user, login_user, login_required
from app.models import User
from flask_login import logout_user


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')

@app.route('/artistlist')
def artistlist():
    artist_list = Artist.query.all()
    event_list = Event.query.all()
    venue_list = Venue.query.all()
    return render_template('artistlist.html', artist_list=artist_list, event_list=event_list, venue_list=venue_list)

@app.route('/newartist', methods=['GET','POST'])
def newartist():
    form = ArtistForm()
    form_results = {}
    if form.validate_on_submit():
        form_results = {
            "name": request.form.get("name"),
            "genre": request.form.get("genre"),
            "bio": request.form.get("bio")
        }
        new_artist = Artist(name=form_results['name'],genre=form_results['genre'],bio=form_results['bio'])
        db.session.add(new_artist)
        db.session.commit()
        return redirect('/')
    return render_template('newartist.html', form=form)
@app.route('/newvenue', methods=['GET','POST'])
def newvenue():
    form = VenueForm()
    form_results = {}
    if form.validate_on_submit():
        form_results = {
            "name": request.form.get("name"),
            "address": request.form.get("address"),
        }
        new_artist = Venue(name=form_results['name'],address=form_results['address'])
        db.session.add(new_artist)
        db.session.commit()
        return redirect('/')
    return render_template('newvenue.html', form=form)
@app.route('/newevent', methods=['GET','POST'])
def newevent():
    form = EventForm()
    form.artists.choices = [(a.id, a.name) for a in Artist.query.all()]
    form.venue.choices = [(v.id, v.name) for v in Venue.query.all()]
    if form.validate_on_submit():
        event_date = form.time.data
        new_event = Event(name=form.name.data, time=event_date, venue_id=form.venue.data)

        artist_ids = form.artists.data

        if not isinstance(artist_ids, (list, tuple)):
            artist_ids = [artist_ids]
        all_artists = Artist.query.all()
        for artist in all_artists:
            for id in artist_ids:
                if id == artist.id:
                    new_event.artists.append(artist)

        db.session.add(new_event)
        db.session.commit()
        return redirect('/')
    return render_template('newevent.html', form=form)

@app.route('/artist/<name>', methods=['GET', 'POST'])
def artist(name):
    event_list = []
    target_artist = Artist.query.filter_by(name=name).first()

    if not target_artist:
        return "Artist not found", 404

    artist_info = {
        'id': target_artist.id,
        "name": target_artist.name,
        "genre": target_artist.genre,
        "bio": target_artist.bio
    }

    for event in target_artist.events:
        event_list.append(event.name)

    return render_template('artist.html', title='Home', artist_info=artist_info, event_list=event_list)



@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

    populate_db()

    return render_template('index.html')

def populate_db():
    s1 = Artist(name='name1', genre='genre1', bio='bio1')
    s2 = Artist(name='name2', genre='genre2', bio='bio2')
    s3 = Artist(name='name3', genre='genre3', bio='bio3')
    s4 = Artist(name='name4', genre='genre4', bio='bio4')
    s5 = Artist(name='name5', genre='genre5', bio='bio5')

    db.session.add_all([s1, s2, s3, s4, s5])
    db.session.commit()

    v1 = Venue(name='venue1', address='address1')
    v2 = Venue(name='venue2', address='address2')
    v3 = Venue(name='venue3', address='address3')
    db.session.add_all([v1, v2, v3])
    db.session.commit()

    e1 = Event(name="event1", time=date(2022, 1, 1), venue_id=v1.id, artists=[s1])
    e2 = Event(name="event2", time=date(2022, 1, 2), venue_id=v2.id, artists=[s2, s3])
    e3 = Event(name="event3", time=date(2022, 1, 3), venue_id=v3.id, artists=[s3])
    e4 = Event(name="event4", time=date(2022, 1, 4), venue_id=v1.id, artists=[s1, s4])
    e5 = Event(name="event5", time=date(2022, 1, 5), venue_id=v2.id, artists=[s2])
    e6 = Event(name="event6", time=date(2022, 1, 6), venue_id=v3.id, artists=[s3, s5])
    e7 = Event(name="event7", time=date(2022, 1, 7), venue_id=v3.id, artists=[s3])

    db.session.add_all([e1, e2, e3, e4, e5, e6, e7])
    db.session.commit()
    return render_template('index.html')
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user.html', user=user, form=form)


