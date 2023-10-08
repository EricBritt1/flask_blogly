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

    post = db.relationship("Posts", backref="Users", cascade="all, delete-orphan")

   


class Posts(db.Model):
    
    __tablename__ = 'Post'
    
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column (db.DateTime, nullable = False, default=datetime.datetime.now)

    user_id = db.Column (db.Integer, db.ForeignKey('user.id'), nullable = False)

    tags = db.relationship('Tag', secondary='PostTags', backref='Post')

    
class Tag(db.Model):

    __tablename__ = 'Tags'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, nullable=False, unique=True)

class PostTag(db.Model):

    __tablename__ = 'PostTags'

    post_id = db.Column(db.Integer, db.ForeignKey('Post.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('Tags.id'), primary_key=True)


def connect_db(app):
    db.app = app
    db.init_app(app)


