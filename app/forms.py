from flask.ext.wtf import Form
from wtforms import StringField, BooleanField,StringField,PasswordField,SubmitField,TextAreaField,FileField,SelectField
from wtforms.validators import DataRequired,Required


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class LoginNew(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    
class WishForm(Form):
    title = StringField('Title', validators=[Required()])
    description = TextAreaField('Description')
    thumbnail = FileField('Custom Image')
    url = StringField('Search For Image')
    status = SelectField('Status',choices=[('0','Not Received'),('1','Received')])
    submit = SubmitField('Add Wish')