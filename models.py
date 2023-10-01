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

def connect_db(app):
    db.app = app
    db.init_app(app)

