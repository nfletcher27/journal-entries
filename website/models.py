from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

# Create a node which takes in a model from our database
class Note(db.Model):
    
    # Our notes have an ID which is our column value, data which is a string of a maximum length, the date of creation, and the user ID
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
# Create a user which takes in our model and a UserMixin which provides easy implementation of authentication and user ID properties
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
