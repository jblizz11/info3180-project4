"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
import os
import time
import datetime
from datetime import *
import json
import requests
import BeautifulSoup 
import bcrypt
import urlparse 
from app import app
from flask import render_template, request, redirect, url_for,jsonify,g,session,flash
from app import db
from werkzeug import secure_filename
from flask.ext.wtf import Form 
from wtforms.fields import TextField, PasswordField,SelectField,FileField# other fields include PasswordField 
from wtforms.validators import Required, Email
from app.models import Myprofile,Wish,User
from app.forms import LoginForm,LoginNew,WishForm,SignUpForm



SECRET_KEY="super secure key"

app.config.from_object(__name__)

## New user Profile Form 

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

## First Page that loads up for App 
@app.route('/')
def index():
    """Render website's home page."""
    return app.send_static_file('index.html')
    
## Signing up Page 
@app.route('/signup', methods=['POST'])
def signup():
    json_data = json.loads(request.data)
    uploadedfile = json_data.get('filepath')
    #get this working
    if uploadedfile:
        uploadedfilename = json_data.get('username') + '_' + secure_filename(uploadedfile.filename)
        filepath = os.path.join(os.getcwd() + '/app/static/uploads/',uploadedfilename)
        uploadedfile.save(filepath)
    else:
        uploadedfilename = '/app/static/img/octocat.png'
    user = User(uploadedfilename,json_data.get('firstname'), json_data.get('lastname'), json_data.get('username'),bcrypt.hashpw(json_data.get('password').encode('utf-8'), bcrypt.gensalt()),json_data.get('email'),datetime.now())
    try:
        db.session.add(user)
        db.session.commit()
        status = "success"
    except:
        status = "This user already exists"
    return jsonify({'result':status})
    
    
#Log in page for a registered user
@app.route('/login', methods=["POST"])
def login():
    json_data = json.loads(request.data)
    user = User.query.filter_by(username=json_data['username']).first()
    print user
    if user and user.password == bcrypt.hashpw(json_data.get('username').encode('utf-8'), user.password.decode().encode('utf-8')):
        session['user'] = user.username
        status = True
    else:
        status = False
    print status
    return jsonify({'logged in': status})

#Log out a user
@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return jsonify({'success': 'logged out'})
    
#View a registered user page
@app.route('/user/<id>',methods=["GET","POST"])
def user(id):
    user = User.query.filter_by(id=id).first()
    image = '/static/uploads/' + user.image
    if request.method == 'POST' or ('Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json'):
        return jsonify(id=user.id, image=user.image,firstname = user.first_name, lastname = user.last_name, username=user.username, email = user.email,addon=user.addon)
    else:
        user = {'id':user.id,'image':user.image, 'firstname':user.first_name, 'lastname': user.last_name, 'username':user.username,'email': user.email,'addon':timeinfo(user.addon)}
        return render_template('userview.html', user=user)

#View all users page
@app.route('/users',methods=["POST","GET"])
def users():
    users = db.session.query(User).all()
    if request.method == "POST" or ('Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json'):
        userlist=[]
        for user in users:
            userlist.append({'id':user.id,'username':user.username})
        return jsonify(users=userlist)
    else:
        return render_template('users.html', users=users)



## Added Routes for Part 3
@app.route('/wish/<id>',methods=["POST"])
def new_wish(id):
    json_data = json.loads(request.data)
    if request.method == 'POST':
        uploadedfile = request.files['thumbnail']
        if uploadedfile:
            uploadedfilename = '_' + secure_filename(uploadedfile.filename)
            filepath = os.path.join(os.getcwd() + '/app/static/wishuploads/',uploadedfilename)
            uploadedfile.save(filepath)
        elif not uploadedfile and form.url.data!="":
            return images(get_images(form.url.data))
            uploadedfilename = '_' + secure_filename(uploadedfile.filename)
            filepath = os.path.join(os.getcwd() + '/app/static/wishuploads/', uploadedfilename)
            uploadedfile.save(filepath)
        else:
            uploadedfile = ""
        wish = Wish(1,uploadedfilename,json_data.get('title'), json_data.get('description'),json_data.get('status'),datetime.now())
        db.session.add(wish)
        db.session.commit()
        # return images(get_images(form.url.data))
    else:
        return render_template('wishadd.html',form=form)
    
@app.route('/wishes/',methods=["POST","GET"])
def wishes():
    wishes = db.session.query(Wish).all()
    if request.method == "POST" or ('Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json'):
        wishlist=[{'id':user.id}]
        for wish in wishes:
            wishlist.append({'title':wish.name,'description':wish.description})
        return jsonify(wishes=wishlist)
    else:
        return render_template('wishes.html', wishes=wishes)        

@app.route('/images', methods=['POST'])
def get_images():
    json_data = json.loads(request.data)
    url = json_data.get('url')
    soup = BeautifulSoup.BeautifulSoup(requests.get(url).text)
    images = BeautifulSoup.BeautifulSoup(requests.get(url).text).findAll("img")
    urllist = []
    og_image = (soup.find('meta', property='og:image') or soup.find('meta', attrs={'name': 'og:image'}))
    if og_image and og_image['content']:
        urllist.append(urlparse.urljoin(url, og_image['content']))
    thumbnail_spec = soup.find('link', rel='image_src')
    if thumbnail_spec and thumbnail_spec['href']:
        urllist.append(urlparse.urljoin(url, thumbnail_spec['href']))
    for image in images:
        if "sprite" not in image["src"]:
            urllist.append(urlparse.urljoin(url, image["src"]))
    print urllist
    return jsonify(imagelist=urllist)
            

@app.route('/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            return jsonify({'status': True})
    else:
        return jsonify({'status': False})


@app.route('/logins/', methods=["GET", "POST"])
def logins():
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
    

# this is in accordance with project 1 &2
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
    image = '/static/uploads/' + profile.image
    if request.method == 'POST':
        return jsonify(id=profile.id,username=profile.user_name,image=image,sex=profile.sex, age=profile.age,profile_add_on=timeinfo(profile.profile_add_on),highscore=profile.high_score, tdollars=profile.tdollars)
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