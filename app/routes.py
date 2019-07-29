from app import app, db
from flask import render_template, url_for, flash, redirect, request
from app.forms import LoginForm, RegForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Posts
from werkzeug.urls import url_parse
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from ocr import ocr_core


# define a folder to store and later serve the images
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'app/static/uploads/')

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me = {}'.format(
            form.username.data, form.remember_me.data
        ))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('reg.html', title='Register', form=form)
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
    # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected', title='Upload')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected', title='Upload')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            option = request.form['options']
            lang = request.form.getlist('lang')
            # call the OCR function on it
            extracted_text = (ocr_core(file.filename, option, lang).split('\n'))
            # extract the text and display it
            return render_template('upload.html',
                                    msg='Successfully processed',
                                    extracted_text=extracted_text,
                                    img_src=filename,
                                    option=option,
                                    file=file.filename,
                                    lang=lang)
    elif request.method == 'GET':
        return render_template('upload.html', title='Upload')
@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html', images=Posts.query.all(), title='Home')
@app.route('/save_image', methods=['POST'])
@login_required
def save_image():
    u = current_user.get_id()
    user = User.query.get(u)
    img = Posts(image_file=request.form['image_path'], body=request.form['txtArea'], author=user)

    db.session.add(img)
    db.session.commit()
    # print(Image.query.all())
    return redirect(url_for('index'))
@app.route('/about')
def about():
    return render_template('about.html', title='About')
@app.route('/edit')
def edit():
    return render_template('edit.html', images=Posts.query.all(), title='Edit')