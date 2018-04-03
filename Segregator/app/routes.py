from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm,RegistrationForm,FeedbackForm
from app.models import User,Feedback
import os,math


@app.route('/display')
@login_required
def display():
	filename=request.args.get('file')
	foldername=request.args.get('folder')
	filename=foldername+filename
	return render_template('display.html',files=filename)


@app.route('/dashboard')
@login_required
def dashboard():
	folders=[i for i in  os.listdir(os.path.join(app.static_folder))]
	folders.remove('styles')
	rows=len(folders)
	return render_template('dashboard.html',folders=folders,rows=rows)


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
		if form.passkey.data==app.config['REGISTRATION_KEY']:
			user = User(username=form.username.data, email=form.email.data)
			user.set_password(form.password.data)
			db.session.add(user)
			db.session.commit()
			flash('Congratulations, you are now a registered user!')
			return redirect(url_for('login'))
		flash('Invalid Passkey!')
		return redirect(url_for('register'))
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
		msg=Feedback(feedback=form.feedback.data,author=current_user)
		db.session.add(msg)
		db.session.commit()
		flash('Message sent succesfully!')
		return redirect(url_for('feedback'))
	page = request.args.get('page', 1, type=int)
	msgs = Feedback.query.order_by(Feedback.timestamp.desc()).paginate(page,6 , False) # 6 is the posts per page
	next_url = url_for('feedback', page=msgs.next_num) if msgs.has_next else None
	prev_url = url_for('feedback', page=msgs.prev_num) if msgs.has_prev else None
	return render_template('feedback.html',form=form,posts=msgs.items,next_url=next_url, prev_url=prev_url)