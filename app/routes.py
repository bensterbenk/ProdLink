import datetime
import json
import os
import shutil
import traceback
from datetime import datetime
from datetime import date
from random import choice

from flask import Blueprint, render_template, flash, redirect, request, url_for, current_app, Response, \
    send_from_directory
from sqlalchemy import or_
from .forms import LoginForm, RegistrationForm, EmptyForm, PostForm, SearchForm, CommentForm
from app import app, models
from app import db
from flask_login import current_user, login_user, login_required
from app.models import User, Post, Tag, Comment
from flask_login import logout_user
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
<<<<<<< Updated upstream

    return render_template("index.html", title='Home Page')
=======
    data = {'message': 'This data comes from a JSON response.'}
    return jsonify(data)
>>>>>>> Stashed changes

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
    prodwizard = User.query.filter_by(username='prodwizard').first()

    # Example titles and bodies for different types of tracks
    example_titles = [
        "Chill Vibes on a Sunday",
        "Epic Guitar Solo",
        "Lofi Beats for Studying",
        "Soulful R&B Melody",
        "Hype Hip-Hop Party",
        "Experimental Drum and Bass",
        "Acoustic Guitar Serenade",
        "Piano Sonata in C Minor",
        "Vocals of the Heart",
        "Deep Bass Groove",
        "Dynamic Drum Patterns",
        "Melancholic Sad Symphony",
        "Happy Uplifting Harmony",
        "Energetic Hype Anthem",
        "Mellow Evening Jazz"
    ]

    example_bodies = [
        "Sit back and relax with this chill track. Perfect for a lazy Sunday afternoon.",
        "Get ready for an epic guitar solo that will blow your mind!",
        "Need some background music for studying? Check out these calming lofi beats.",
        "Experience the soulful vibes of this R&B melody. Smooth and captivating.",
        "Turn up the volume and join the hip-hop party! Hype beats and catchy lyrics await.",
        "Dive into the world of experimental drum and bass with this mind-bending track.",
        "Let the acoustic guitar serenade you with its soothing melodies.",
        "Immerse yourself in the beauty of this piano sonata in C minor. A classical masterpiece.",
        "Feel the emotions with powerful vocals that speak to the heart.",
        "Groove to the deep bass and let the rhythm take over your senses.",
        "Dynamic drum patterns that will keep you moving and grooving.",
        "A symphony of melancholic notes that will tug at your heartstrings.",
        "Need a mood boost? Listen to this happy and uplifting harmony.",
        "Get ready for an energetic hype anthem that will lift your spirits.",
        "Unwind with mellow evening jazz. Perfect for a laid-back atmosphere."
    ]

    for i in range(15):
        # Choose a random tag for each post
        tags = [choice([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15])]

        # Choose a random audio file for each post
        audio_file = choice(["p1_audio.mp3", "p2_audio.mp3", "corleo_attempt.mp3", "jersey_1.mp3", "hard_but_soft.mp3"])

        # Create and add the new post to the database
        new_post = Post(title=example_titles[i], body=example_bodies[i], user_id=prodwizard.id, tags=tags,
                        audio_file=audio_file)
        db.session.add(new_post)

    # Commit changes to the database
    db.session.commit()
    return render_template('index.html')

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

@app.route('/samplesforum', methods=['GET', 'POST'])
def samples_forum():
    form = SearchForm()
    form.genretags.choices = [(a.id, a.name) for a in Tag.query.filter_by(tag_type='genre')]
    form.instrtags.choices = [(a.id, a.name) for a in Tag.query.filter_by(tag_type='instr')]
    form.moodtags.choices = [(a.id, a.name) for a in Tag.query.filter_by(tag_type='mood')]
    posts_display = Post.query.all()

    if form.validate_on_submit():
        posts_display = []
        search_text = form.title.data.lower()
        tag_ids = form.genretags.data + form.moodtags.data + form.instrtags.data
        if not isinstance(tag_ids, (list, tuple)):
            tag_ids = [tag_ids]

        if tag_ids and search_text:
            tagged_posts = Post.query.filter(Post.tags.any(Tag.id.in_(tag_ids))).all()
            text_search_posts = Post.query.filter(
                or_(Post.title.ilike(f'%{search_text}%'), Post.body.ilike(f'%{search_text}%'))).all()
            tagged_post_ids = set(post.id for post in tagged_posts)
            text_search_post_ids = set(post.id for post in text_search_posts)
            common_post_ids = tagged_post_ids.intersection(text_search_post_ids)
            common_posts = [post for post in tagged_posts if post.id in common_post_ids]
            posts_display.extend(common_posts)
        else:
            if tag_ids:
                tagged_posts = Post.query.filter(Post.tags.any(Tag.id.in_(tag_ids))).all()
                posts_display.extend(tagged_posts)
            else:
                text_search_posts = Post.query.filter(
                    or_(Post.title.ilike(f'%{search_text}%'), Post.body.ilike(f'%{search_text}%'))).all()
                posts_display.extend(text_search_posts)

    # Check if the request is a POST and return JSON response
    if request.method == 'POST':
        posts_data = [{'id': post.id, 'title': post.title, 'body': post.body, 'author': post.author.username} for post in posts_display]
        return jsonify({'posts': posts_data})

    # Render the template for GET request
    return render_template('samplesforum.html', form=form, posts=posts_display)

    # Remove duplicate posts in case a post matches both tag and text criteria
    posts_display = list(set(posts_display))
    return render_template('samplesforum.html', form=form, posts=posts_display)
@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    form = CommentForm()
    tag_list = []
    comment_list = []
    target_post = Post.query.filter_by(id=post_id).first()
    target_user = User.query.filter_by(id=target_post.user_id).first()
    if not target_post:
        return "Post not found", 404
<<<<<<< Updated upstream
    if form.validate_on_submit():
        new_comment = Comment(body=form.body.data, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        target_post.comments.append(new_comment)
=======
    for tag in target_post.tags:
        tag_list.append(tag.name)
    for comment in target_post.comments:
        comment_info = {"body": comment.body, "author": (User.query.filter_by(id=comment.user_id).first()).username}
        comment_list.append(comment_info)
>>>>>>> Stashed changes

    post_info = {
        'id': target_post.id,
        "title": target_post.title,
        "body": target_post.body,
        "author": target_user.username,
        "timestamp": target_post.timestamp,
        "audio_file": target_post.audio_file
    }
    for tag in target_post.tags:
        tag_list.append(tag.name)
    for comment in target_post.comments:
        comment_info = {"body": comment.body, "author": (User.query.filter_by(id=comment.user_id).first()).username}
        comment_list.append(comment_info)


    return render_template('post.html', post_info=post_info, tag_list=tag_list, comment_list=comment_list, form=form)
@app.route('/posts')
def posts():
    posts = Post.query.all()
<<<<<<< Updated upstream
    return render_template('posts.html', posts=posts)
=======
    posts_info = []
    for post in posts:
        target_user = User.query.filter_by(id=post.user_id).first()
        tag_list = []
        comment_list = []
        for tag in post.tags:
            tag_list.append(tag.name)
        for comment in post.comments:
            comment_info = {"body": comment.body, "author": (User.query.filter_by(id=comment.user_id).first()).username}
            comment_list.append(comment_info)
        post_info = {
            'id': post.id,
            "title": post.title,
            "body": post.body,
            "author_name": target_user.username,
            "author_id": target_user.id,
            "timestamp": post.timestamp,
            "audio_file": post.audio_file,
            "tags": tag_list,
            "comments": comment_list
        }
        posts_info.append(post_info)
    return jsonify(posts_info)
>>>>>>> Stashed changes
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

        # Save audio file
        audio_file = form.audio_file.data
        post.save_audio(audio_file)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect('/')
    return render_template('newpost.html', form=form)
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/static/audio/<filename>')
def serve_audio(filename):
<<<<<<< Updated upstream
    return send_from_directory(app.root_path, f'static/audio/{filename}')
=======
    return send_from_directory(app.root_path, f'static/audio/{filename}')

@app.route('/api/tags')
def all_tags():
    all_tags = Tag.query.all()
    tag_data = [{'id': tag.id, 'name': tag.name, 'tag_type': tag.tag_type} for tag in all_tags]
    return jsonify({'tags': tag_data})

@app.route('/api/tags/<tag_id>', methods=['GET', 'POST'])
def tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()

    tag_posts = tag.posts
    tag_posts_ids = []
    for post in tag_posts:
        tag_posts_ids.append(post.id)
    tag_info = {
        'id':tag.id,
        'name': tag.name,
        'posts': tag_posts_ids,
        'tag_type': tag.tag_type
    }
    return tag_info

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()

    # Extract registration data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if username or email already exists
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'error': 'Username or email already exists'}), 400

    # Create a new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201

@app.route('/api/login', methods=['POST'])
def login_user_route():
    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        # Replace 'User' with the actual model you are using
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # Create JWT token and send it to the client
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify(message='Invalid credentials'), 401
@app.route('/api/logout')
@login_required
def logout_user_route():
    # Log out the user
    logout_user()

    return jsonify({'message': 'Logout successful'}), 200


@app.route('/api/newpost', methods=['POST'])
def newpostapi():
    try:
        # Access form data using request.form
        title = request.form.get('title')
        post_body = request.form.get('post')

        # Handle audio file
        audio_file = request.files.get('audio_file')
        print(audio_file)

        # Convert user id to integer (assuming there is at least one user)
        user_id = int(User.query.all()[0].id)

        # Create a new post
        post = Post(title=title, body=post_body, user_id=user_id)
        post.save_audio(audio_file)

        # Add tags to the post
        tag_ids = json.loads(request.form.get('genretags', '[]')) + \
                  json.loads(request.form.get('moodtags', '[]')) + \
                  json.loads(request.form.get('instrtags', '[]'))

        if not isinstance(tag_ids, (list, tuple)):
            tag_ids = [tag_ids]

        all_tags = Tag.query.all()
        for tag in all_tags:
            for tag_id in tag_ids:
                if tag_id == tag.id:
                    post.tags.append(tag)

        # Save the post to the database
        db.session.add(post)
        db.session.commit()

        return jsonify({'message': 'Post created successfully'}), 201

    except Exception as e:
        # Log the error traceback for debugging
        app.logger.error(f"Error creating post: {e}")
        app.logger.error(traceback.format_exc())

        return jsonify({'error': 'Internal Server Error'}), 500
@app.route('/api/check-auth')
@cross_origin(supports_credentials=True)
def check_authentication():
    if current_user.is_authenticated:
        return jsonify({'authenticated': True, 'username': current_user.username})
    else:
        return jsonify({'authenticated': False})

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(datetime.timezone.utc)
        target_timestamp = datetime.timestamp(now + datetime.timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response
@app.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return {"msg": "Wrong email or password"}, 401

    access_token = create_access_token(identity=email)
    response = {"access_token":access_token}
    return response

@app.route('/profile')
@jwt_required()
def my_profile():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body
@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response
>>>>>>> Stashed changes
