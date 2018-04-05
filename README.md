# Waste Segregator Web application

This repository contains the source code for the Waste Segregator web application which is a CRUD app built using Flask frmaework.

<h2>Features -</h2>
<li>
  Homepage and About section that describes the aim and operation of the project.
</li>

<li>
  Dashboard that provides admin priviliges to view the archived test results.
</li>
<li>
  Sign In and Register functionality with Feedback feature.
</li>

<h2> Requirements </h2>

* Python 3

* Flask

* Flask plugins - SQLAlchemy , migrate, wtforms, login

* HTML/CSS, Bootstrap.

<h2> Installation </h2>

Type the following command to pull the git repository using terminal-

```
git pull https://github.com/boudhayan-dev/Segregator-FlaskApp 
```
Navigate inside the folder -
```
cd Segregator-FlaskApp
```
Set the flask variable -
```
set FLASK_APP=run.py
```

Perform Database migration -
```
flask db init
flask db migrate -m "new db"
flask db upgrade
```

Run the flask app -
```
flask run
```

