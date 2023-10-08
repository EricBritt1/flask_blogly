"""Blogly application."""

import logic
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Posts, Tag, PostTag
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.app_context().push()


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "GOTEMLOLOLOLOL"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return redirect('/users')

@app.route('/users')
def users_listing():
    users = Users.query.all()
    return render_template('users.html', users=users)

@app.route('/users_form')
def users_form():

    return render_template('users_form.html')

@app.route('/users_form', methods = ["POST"])
def get_users_form_info():
    first_name = request.form['First']
    last_name = request.form['Last']
    image_url = request.form['ImgUrl']

    new_user = Users(first_name=first_name, last_name=last_name, image_url=image_url or None)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = Users.query.get_or_404(user_id)
    posts = Posts.query.filter(Posts.user_id==user_id)
    print(posts)
    return render_template('user-detail.html', user=user, posts=posts)

@app.route('/hello/<int:user_id>/edit')
def test_template(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template('fix_user.html', user=user)

@app.route('/hello/<int:user_id>/edit', methods = ["POST"])
def updated_user(user_id):
    user = Users.query.get_or_404(user_id)
    user.first_name = request.form['First']
    user.last_name = request.form['Last']
    user.image_url = request.form['ImgUrl']
    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/hello/<int:user_id>/delete', methods = ['GET','POST'])
def delete_user(user_id):
    # post = Posts.query.get_or_404(user_id)
    # db.session.delete(post)
    # db.session.commit()
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/')

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    user = Users.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('post_form.html', user=user, tags=tags)

# In solution for this specific route user=user inside of new_post. For some reason the argument didn't work properly. How could I fix that?
@app.route('/users/<int:user_id>/posts/new', methods = ["POST"] )
def result_show_post_form(user_id):
    user = Users.query.get_or_404(user_id)
    # How does this work? I know how .getlist operates but, I've never seen int(num) used witb it before the for statement. What does that do?
    # This gets me the integer values from my form AKA the tag IDs so I can access them in tags
    tags_to_add_id =[int(num) for num in request.form.getlist('Name')]
    tags = Tag.query.filter(Tag.id.in_(tags_to_add_id)).all()
    new_post = Posts(title=request.form['Title'], content=request.form['Content'], user_id=user.id, tags=tags)
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_a_post(post_id):
    post = Posts.query.get_or_404(post_id)

    return render_template('post_page.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_a_post(post_id):
    post = Posts.query.get_or_404(post_id)
    tags =Tag.query.all()

    return render_template('edit_post_form.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods = ["POST"])
def edited_a_post(post_id):
    post = Posts.query.get_or_404(post_id)
    post.title = request.form['post_title']
    post.content = request.form['post_content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods = ['POST'])
def delete_a_post(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def list_all_tags():
    tags = Tag.query.all()

    return render_template('tag_list.html', tags=tags)

@app.route('/tag_form')
def create_tag_form_get():

    return render_template('create_tag_form.html')

@app.route('/tag_form', methods = ['POST'])
def create_tag_form_post():

    tag_name = request.form['Name']
    new_tag_name = Tag(name=tag_name)
    db.session.add(new_tag_name)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def tag_detail_page(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_detail_page.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form_get(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit_tag_form.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods = ['POST'])
def edit_tag_form_post(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['Name']
    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags/{tag.id}')

@app.route('/tags/<int:tag_id>/delete', methods = ['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')
