from . import db  
class Myprofile(db.Model):     
    id = db.Column(db.Integer, primary_key=True)     
    first_name = db.Column(db.String(80))     
    last_name = db.Column(db.String(80)) 
    age = db.Column(db.Integer)    
    sex =db.Column(db.String(20))
    image= db.Column(db.String(120))
    email = db.Column(db.String(120),index=True, unique=True)
    password =db.Column(db.String(45),unique=True) 
 
 
    
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
        return '<User %r>' % (self.nickname)