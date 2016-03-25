from . import db  
class Myprofile(db.Model): 
    id = db.Column(db.Integer, primary_key=True)     
    first_name = db.Column(db.String(80))     
    last_name = db.Column(db.String(80)) 
    age = db.Column(db.Integer)    
    sex =db.Column(db.String(20))
    image= db.Column(db.String(120))
    user_name=db.Column(db.String(40))
    profile_add_on=db.Column(db.DateTime,nullable=False)
    high_score=db.Column(db.Integer)
    tdollars=db.Column(db.Integer)
    #image=db.Column(db.LargeBinary)
    email = db.Column(db.String(120),index=True, unique=True)
    password =db.Column(db.String(45),unique=True) 
    wishes=db.relationship('Wish',backref='myprofile',lazy='dynamic')
    
    def __init__(self,image,user_name,first_name,last_name,age,sex,profile_add_on,password,email):
        self.image = image
        self.user_name = user_name
        self.first_name = first_name
        self.last_name= last_name
        self.age = age
        self.sex = sex
        self.userhighscore = 0
        self.usertdollars = 0
        self.profile_add_on=profile_add_on
        self.password=password
        self.email=email
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<id {}>'.format(self.id)
        
        
class Wish(db.Model):
    __tablename__ = 'wishes'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('Myprofile.id'))
    image = db.Column(db.String(255))
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    status = db.Column(db.Boolean)
    addon = db.Column(db.DateTime,nullable=False)
    
    
    def __init__(self,userid,image,name,description,status,addon):
        self.userid = userid
        self.image = image
        self.name = name
        self.description = description
        self.status = status
        self.addon = addon
    
    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Wish %r>' % (self.name)