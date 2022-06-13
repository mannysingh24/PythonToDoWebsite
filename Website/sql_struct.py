from flask_login import UserMixin
from . import database
from sqlalchemy.sql import func

class Note(database.Model):
    user_id = database.Column(database.Integer, database.ForeignKey('user.id')) #must pass a valid id when passing a note object (1 user with many notes)
    id = database.Column(database.Integer, primary_key=True)
    data = database.Column(database.String(10000))
    note_date = database.Column(database.DateTime(timezone=True), default=func.now())


class User(database.Model, UserMixin):
    email = database.Column(database.String(150), unique=True) #no user can have the same email
    password = database.Column(database.String(150))
    first_name = database.Column(database.String(150))
    last_name = database.Column(database.String(150))
    id = database.Column(database.Integer, primary_key=True)
    notes = database.relationship('Note') #list that stores all the different notes for each user
