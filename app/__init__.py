import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI']='postgres://ojzmhgzqgzxjmk:lhE-r3F0cCZOcaoaseIPSFaE9Q@ec2-54-83-198-159.compute-1.amazonaws.com:5432/db0p2461btcvuh'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://project3:project3@localhost/project3"
db = SQLAlchemy(app)
db.create_all()


from app import views, models 
