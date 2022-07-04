from flask import render_template, redirect, url_for, flash, request, abort
from awarenesscommunity import app, database, bcrypt
from awarenesscommunity.forms import FormSignin, FormSignup, FormEditProfile, FormPostCreation
from awarenesscommunity.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route("/", methods=['GET', 'POST'])
@login_required
def home():
    lista_de_usuarios = User.query.all()
    posts = Post.query.order_by(Post.id.desc())
    form = FormPostCreation()
    profile_picture = url_for('static', filename="photos_profile/{}".format(current_user.profile_picture))
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Text posted successfully!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('home.html', posts=posts, form=form, profile_picture=profile_picture, lista_de_usuarios=lista_de_usuarios)

@app.route("/contato", methods=['GET', 'POST'])
@login_required
def contato():
    posts = Post.query.order_by(Post.id.desc())
    form = FormPostCreation()
    profile_picture = url_for('static', filename="photos_profile/{}".format(current_user.profile_picture))
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Text posted successfully!', 'alert-success')
        return redirect(url_for('contato'))
    return render_template('contato.html', posts=posts, profile_picture=profile_picture, form=form)


@app.route("/usuarios")
@login_required
def usuarios():
    lista_de_usuarios = User.query.all()
    return render_template('usuarios.html', lista_de_usuarios=lista_de_usuarios)


@app.route("/login", methods=['GET', 'POST'])
def signin():
    form_signin = FormSignin()
    form_signup = FormSignup()

    if form_signin.validate_on_submit() and 'button_submit_signin' in request.form:
        user = User.query.filter_by(email=form_signin.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_signin.password.data):
            login_user(user, remember=form_signin.keep_logged.data)
            flash(f'{form_signin.email.data} logged in successfully!', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('log in failed! Incorrect email or password!', 'alert-danger')
    if form_signup.validate_on_submit() and 'button_submit_signup' in request.form:
        password_crypt = bcrypt.generate_password_hash(form_signup.password.data)
        users = User(username=form_signup.username.data, email=form_signup.email.data, password=password_crypt)
        database.session.add(users)
        database.session.commit()
        flash(f'{form_signup.email.data} successful registration!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('signin.html', form_signin=form_signin, form_signup=form_signup)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Log out successfully!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    profile_picture = url_for('static', filename="photos_profile/{}".format(current_user.profile_picture))
    return render_template('profile.html', profile_picture=profile_picture)


@app.route('/post/write', methods=['GET', 'POST'])
@login_required
def post_write():
    form = FormPostCreation()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Text posted successfully!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('postwrite.html', form=form)


def save_picture(picture):
    script = secrets.token_hex(8)
    name, extension = os.path.splitext(picture.filename)
    name_file = name + script + extension
    full_path = os.path.join(app.root_path, 'static/photos_profile', name_file)
    size = (400, 400)
    compact_picture = Image.open(picture)
    compact_picture.thumbnail(size)
    compact_picture.save(full_path)
    return name_file


def update_courses(form):
    list_courses = []
    for field in form:
        if 'class_' in field.name:
            if field.data:
                list_courses.append(field.label.text)
    return ';'.join(list_courses)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = FormEditProfile()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.profile_picture.data:
            picture_name = save_picture(form.profile_picture.data)
            current_user.profile_picture = picture_name
        current_user.courses = update_courses(form)
        database.session.commit()
        flash('Profile updated successfully!', 'alert-success')
        return redirect(url_for('profile'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    profile_picture = url_for('static', filename="photos_profile/{}".format(current_user.profile_picture))
    return render_template('editprofile.html', profile_picture=profile_picture, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def post_layout(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        form = FormPostCreation()
        if request.method == "GET":
            form.title.data = post.title
            form.body.data = post.body
        elif form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            database.session.commit()
            flash('Post edited successfully!', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        database.session.delete(post)
        database.session.commit()
        flash('Post deleted successfully!', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
