from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm, PostForm
from app.models import User, Post


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)



@app.route('/signup', methods=["GET", "POST"])
def signup():
    # create an instance of the SignUpForm
    form = SignUpForm()
    # Check if a POST request AND data is valid
    if form.validate_on_submit():
        print('Form Submitted and Validated!')
        # Get the data from the form
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(email, username, password)
       # Query our user table to see if there are any users with either username or email from form
        check_user = User.query.filter(
            (User.username == username) | (User.email == email)).all()
        # If the query comes back with any results
        if check_user:
            # Flash message saying that a user with email/username already exists
            flash('A user with that email and/or username already exists.', 'danger')
            return redirect(url_for('signup'))
        # If check_user is empty, creater a new record in the user table
        new_user = User(email=email, username=username, password=password)
        # Flash a success message
        flash(f'Thank you {new_user.username} for signing up!', 'success')
        # redirect back to home
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # get the username and password from form
        username = form.username.data
        password = form.password.data
        print(username, password)
        # Query the user table to check if there is a user with that username
        user = User.query.filter_by(username=username).first()
        # Check if there is a user and that the password is correct
        if user is not None and user.check_password(password):
            # log the user in
            login_user(user)
            flash(f"{user.username} is now logged in", "warning")
            return redirect(url_for('index'))
        else:
            flash(f"Incorrect username and/or password", "danger")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash(f"You have been logged out", "warning")
    return redirect(url_for('index'))


@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
       # get data from form
        title = form.title.data
        body = form.body.data
        print(title, body, current_user)
        # create new post instance so it will add to db
        new_post = Post(title=title, body=body, user_id=current_user.id)
        flash(f"{new_post.title} has been created", "success")
        return redirect(url_for('index'))
    return render_template('create.html', form=form)

@app.route('/posts/<int:post_id>')
def get_post(post_id):
    # post = Posts.query.get_or_404(post_id)
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post.id} does not exist", "danger")
        return redirect(url_for('index'))
    return render_template('post.html', post=post)



@app.route('/posts/<post_id>/edit', methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('index'))
        #make sure post author is the current user
    if post.author != current_user:
        flash(f"You do not have permission to edit this post", "danger")
        return redirect(url_for('index'))
    form = PostForm()
    if form.validate_on_submit():
        # get the form data
        title = form.title.data
        body = form.body.data
        #update the post using .update method
        post.update(title=title, body=body)
        flash(f"{post.title} has been updated!","success")
        return redirect(url_for('get_post', post_id=post.id))
    if request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    return render_template('edit_post.html', post=post , form=form)


@app.route('/posts/<post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('index'))
        #make sure post author is the current user
    if post.author != current_user:
        flash(f"You do not have permission to delete this post", "danger")
        return redirect(url_for('index'))
    post.delete()
    flash(f"{post.title} has been deleted", "info")
    return redirect(url_for('index'))