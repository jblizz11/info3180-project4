from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID, COMMON_PROVIDERS

import urlparse

app = Flask(__name__)
app.config['SECRET_KEY'] = "this is a super secure key"
app.config['OPENID_PROVIDERS'] = COMMON_PROVIDERS
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
# remember to change to heroku's databas
#db_conn= 'postgresql+psycopg2://lab5:lab5@localhost/lab5' 
app.config['SQLALCHEMY_DATABASE_URI'] = url #os.environ['DATABASE_URI']#db_conn
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://yzicurmnvkqqhp:Kpl-6hLvDaRcPCelsrxdmydSgi@ec2-23-21-219-209.compute-1.amazonaws.com:5432/de7vj5i2j9deb1"
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
oid = OpenID(app,'/tmp')

from app import views
