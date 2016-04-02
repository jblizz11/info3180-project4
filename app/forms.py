#from flask_wtf import Form
from wtforms import Form,StringField, BooleanField,StringField,PasswordField,SubmitField,TextAreaField,FileField,SelectField,TextField,validators



#class LoginForm(Form):
    #openid = StringField('openid', validators=[DataRequired()])
    #remember_me = BooleanField('remember_me', default=False)

class LoginNew(Form):
    username = TextField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])

class WishForm(Form):
    title = StringField('Title', [validators.Required()])
    description = TextAreaField('Description')
    thumbnail = FileField('Custom Image')
    url = StringField('Search For Image')
    status = SelectField('Status',choices=[('0','Not Received'),('1','Received')])
    submit = SubmitField('Add Wish')

class ProfileForm(Form):
    uploadedfile = FileField('User Image')
    username = StringField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    email = StringField('Email', [validators.Required()])
    first_name = StringField('First Name', [validators.Required()])
    last_name = StringField('Last Name', [validators.Required()])
    submit = SubmitField('Sign Up')
