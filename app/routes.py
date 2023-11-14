import datetime
from datetime import datetime
from datetime import date
from flask import Blueprint, render_template, flash, redirect, request, url_for
from .forms import LoginForm, RegistrationForm, EmptyForm, PostForm
from app import app, models
from app import db
from flask_login import current_user, login_user, login_required
from app.models import User, Post, Tag
from flask_login import logout_user


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    posts = Post.query.all()
    return render_template("index.html", title='Home Page', posts=posts)

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
    p1 = Tag(name='rnb')
    p2 = Tag(name='pop')
    p3 = Tag(name='hip-hop')
    p4 = Tag(name='soul')
    p5 = Tag(name='drum and bass')

    db.session.add_all([p1, p2, p3, p4, p5])
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

@app.route('/samplesforum')
def samples_forum():
    return render_template('samplesforum.html')
@app.route('/post/<post_id>')
def post_display(post_id):
    return render_template('post.html')
@app.route('/newpost', methods=['GET','POST'])
def newpost():
    form = PostForm()
    form.tags.choices = [(a.id, a.name) for a in Tag.query.all()]
    if form.validate_on_submit():
        post = Post(body=form.post.data, user_id=current_user.id)
        tag_ids = form.tags.data

        if not isinstance(tag_ids, (list, tuple)):
            artist_ids = [tag_ids]
        all_tags = Tag.query.all()
        for tag in all_tags:
            for id in tag_ids:
                if id == tag.id:
                    post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect('/')
    return render_template('newpost.html', form=form)
@app.route('/about')
def post():
    return render_template('about.html')

