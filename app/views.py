"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
import os
import time
import datetime
#from datetime import *
import json
from app import app
from flask import render_template, request, redirect, url_for,jsonify,g,session,flash
from app import db

from flask.ext.wtf import Form 
from wtforms.fields import TextField, PasswordField,SelectField,FileField# other fields include PasswordField 
from wtforms.validators import Required, Email
from app.models import Myprofile
from app.forms import LoginForm,LoginNew



SECRET_KEY="super secure key"

app.config.from_object(__name__)

class ProfileForm(Form):
     first_name = TextField('First Name', validators=[Required()])
     last_name = TextField('Last Name', validators=[Required()])
     age = TextField('Age', validators=[Required()])
     sex=SelectField(u'Sex',choices=[('M','Male'),('F','Female')])
     user_name= TextField('User Name', validators=[Required()])
     email_name = TextField('Email Name', validators=[Required()])
     password_name = PasswordField('Password Name', validators=[Required()])
     image        = FileField(u'Image File')
     #description  = TextAreaField(u'Image Description')    
     # evil, don't do this
     ##image = TextField('Image', validators=[Required(), Email()])



@app.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginNew(request.form)
    error = None 
    if request.method == "POST":
       
    # change this to actually validate the user
        usernameform= form.username.data 
        userdatabase= Myprofile.query.filter(Myprofile.email == usernameform).one()
       
   #if form.username.data:
        # login and validate the user...
        if request.form['username'] != userdatabase.email:
            error = 'Invalid username' 
        elif request.form['password'] != userdatabase.password:
            error = 'Invalid password' 
        else: 
            session['logged_in'] = True
            flash('You were logged in') 
          
            return redirect(url_for ('profile'))
        # missing
        # based on password and username
        # get user id, load into session
       # user = load_user("1")
      #  login_user(user)
        #flash("Logged in successfully.")
        #return redirect(request.args.get("next") or url_for("home"))
    return render_template("login.html",form=form,error=error)
    
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/profile/', methods=['POST','GET'])
def profile_add():
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age_name = request.form['age']
        email_name = request.form['email_name']
        option_name= request.form['sex']
        password_name = request.form['password_name']
    
        user_name=request.form['user_name']
        form = ProfileForm(request.form)
        
        image_data = request.files[form.image.name].read()
        #form.image.file.save(os.path.join("app/static/uploads", image_data))
        file = request.files[form.image.name]
        filename = file.filename
        file.save(os.path.join("app/static/uploads", filename))
        #open(os.path.join("app/static/uploads", form.image.data), 'w').write(image_data)
        # write the information to the database
        newprofile = Myprofile(first_name=first_name,
                               last_name=last_name,age=age_name,sex=option_name,user_name=user_name,profile_add_on=datetime.now(),email=email_name,image=filename,password=password_name)
        db.session.add(newprofile)
        db.session.commit()

        return redirect('/profile/'+str(Myprofile.query.filter_by(user_name=newprofile.user_name).first().id))

    form = ProfileForm()
    return render_template('profile_add.html',
                           form=form)

@app.route('/profiles/',methods=["POST","GET"])
def profile_list():
    profiles = db.session.query(Myprofile).all()
    if request.method == "POST":
        profilelist=[]
        for profiles in profiles:
            profilelist.append({'id':profiles.id,'username':profiles.user_name})
        return jsonify(profiles=profilelist)
    else:
        
        return render_template('profile_list.html',
                            profiles=profiles)

@app.route('/profile/<userid>')
def profile_view(userid):
    profile = Myprofile.query.filter(Myprofile.id==userid).one()
    if request.method == 'POST':
        return jsonify(id=profile.id,username=profile.user_name, sex=profile.sex, age=profile.age,profile_add_on=timeinfo(profile.profile_add_on),highscore=profile.high_score, tdollars=profile.tdollars)
    else:
        date=timeinfo(profile.profile_add_on)
        profile={'id': profile.id,'username': profile.user_name,'first_name':profile.first_name,'last_name':profile.last_name, 'sex': profile.sex, 'age': profile.age,'profile_add_on':date,'highscore': profile.high_score, 'tdollars': profile.tdollars}
        return render_template('profile_view.html',profile=profile)
    



@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')



def timeinfo(entry):
    day = time.strftime("%a")
    date = time.strftime("%d")
    if (date <10):
        date = date.lstrip('0')
    month = time.strftime("%b")
    year = time.strftime("%Y")
    return day + ", " + date + " " + month + " " + year



###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")