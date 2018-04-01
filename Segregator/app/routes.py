from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm,RegistrationForm,FeedbackForm
from app.models import User,Feedback
import os,math
from PIL import Image


@app.route('/display')
@login_required
def display():
	filename=request.args.get('file')
	foldername=request.args.get('folder')
	filename=foldername+filename
	width,height=(Image.open(os.path.join(app.static_folder,filename))).size
	return render_template('display.html',files=filename,width=width,height=height)


@app.route('/dashboard')
@login_required
def dashboard():
	folders=[i for i in  os.listdir(os.path.join(app.static_folder))]
	return render_template('dashboard.html',folders=folders)


@app.route('/image/<im>')
@login_required
def image(im):
	image_src=[im+'/'+i for i in  os.listdir(os.path.join(app.static_folder,im))]
	rows=math.ceil(len(image_src)/3)
	print(image_src)
	return render_template('dashboard.html',title='Welcome',images=image_src,rows=rows)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html',title='Welcome')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password!')
			return redirect(url_for('login'))
		login_user(user,remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html',title='Sign In',form=form)

@app.route("/register", methods=['GET','POST'])
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

@app.route("/about",methods=['GET', 'POST'])
@login_required
def about():
	return render_template("about.html")

@app.route("/feedback",methods=['GET','POST'])
@login_required
def feedback():
	form=FeedbackForm()
	if form.validate_on_submit():
		flash('Message sent succesfully!')
		return redirect(url_for('feedback'))

	return render_template('feedback.html',form=form)