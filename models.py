import datetime
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

"""Models for Blogly."""

DEFAULT_IMAGE_URL = "https://www.pngkey.com/png/detail/21-213224_unknown-person-icon-png-download.png"


# MODELS GO BELOW!

class Users(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    first_name = db.Column(db.Text, nullable=False)

    last_name = db.Column(db.Text, nullable=False)
    
    image_url = db.Column(db.Text, nullable=False, 
    default=DEFAULT_IMAGE_URL)

   


class Posts(db.Model):
    
    __tablename__ = 'Post'
    
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column (db.DateTime, nullable = False, default=datetime.datetime.now)

    user_id = db.Column (db.Integer, db.ForeignKey('user.id'), nullable = False)

    
    
def connect_db(app):
    db.app = app
    db.init_app(app)


