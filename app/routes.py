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

    return render_template("index.html", title='Home Page')

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
    t1 = Tag(name='rnb', tag_type="genre")
    t2 = Tag(name='pop', tag_type="genre")
    t3 = Tag(name='hip-hop', tag_type="genre")
    t4 = Tag(name='soul', tag_type="genre")
    t5 = Tag(name='drum and bass', tag_type="genre")
    t6 = Tag(name='guitar', tag_type="instr")
    t7 = Tag(name='piano', tag_type="instr")
    t8 = Tag(name='vocals', tag_type="instr")
    t9 = Tag(name='bass', tag_type="instr")
    t10 = Tag(name='drums', tag_type="instr")
    t11 = Tag(name='sad', tag_type="mood")
    t12 = Tag(name='happy', tag_type="mood")
    t13 = Tag(name='hype', tag_type="mood")
    t14 = Tag(name='mellow', tag_type="mood")
    t15 = Tag(name='soulful', tag_type="mood")

    db.session.add_all([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15])
    db.session.commit()

    u1 = User(username='prodwizard', email='prodwizard@wizard.com')
    u1.set_password('wizardman1')
    u2 = User(username='top_op2', email='hater@hating.com')
    u2.set_password('midrick2')

    db.session.add_all([u1, u2])
    db.session.commit()
    p1 = Post(title="Intro to Prodwizard", body='Im the prodwizard! boooo', user_id=u1.id, tags=[t1, t6, t11])
    p2 = Post(title="Only good takes", body='drill is all mid now LMFAOAOAO W lil mabu', user_id=u2.id, tags=[t2, t7, t12])
    db.session.add_all([p1, p2])
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
    active_user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user.html', user=active_user, form=form)

@app.route('/samplesforum')
def samples_forum():
    return render_template('samplesforum.html')
@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    tag_list = []
    target_post = Post.query.filter_by(id=post_id).first()
    target_user = User.query.filter_by(id=target_post.user_id).first()
    if not target_post:
        return "Post not found", 404

    post_info = {
        'id': target_post.id,
        "title": target_post.title,
        "body": target_post.body,
        "author": target_user.username,
        "timestamp": target_post.timestamp
    }

    for tag in target_post.tags:
        tag_list.append(tag.name)

    return render_template('post.html', post_info=post_info, tag_list=tag_list)
@app.route('/posts')
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)
@app.route('/newpost', methods=['GET','POST'])
def newpost():
    form = PostForm()
    form.genretags.choices = [(a.id, a.name) for a in Tag.query.filter_by(tag_type='genre')]
    form.instrtags.choices = [(a.id, a.name) for a in Tag.query.filter_by(tag_type='instr')]
    form.moodtags.choices = [(a.id, a.name) for a in Tag.query.filter_by(tag_type='mood')]
    if form.validate_on_submit():
        post = Post(title = form.title.data, body=form.post.data, user_id=current_user.id)
        tag_ids = form.genretags.data + form.moodtags.data + form.instrtags.data
        if not isinstance(tag_ids, (list, tuple)):
            tag_ids = [tag_ids]
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
def about():
    return render_template('about.html')

