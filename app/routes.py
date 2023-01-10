from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm


@app.route('/')
def index():
    fruits = ['apple', 'banana', 'kiwi', 'strawberry', 'watermelon', 'pineapple']
    return render_template('index.html', name='Tyler', fruits=fruits)
    
@app.route('/posts')
def posts():
    return 'these are the post'

@app.route('/signup', methods = ["GET", "POST"])
def signup():
    #create an instance of the SignUpForm
    form = SignUpForm()
    #Check if a POST request AND data is valid
    if form.validate_on_submit():
        print('Form Submitted and Validated!')
        # Get the data from the form
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(email, username, password)
        # TODO: Check to see if there is a User with the username in the database
        if username == 'Ty.Codes':
            flash('That user already exists', 'danger')
            return redirect(url_for('signup'))
        # TODO: Create a new User with form data and add to database
        # Flash a success message
        flash('Thank you for signing up!', 'success')
        # redirect back to home
        return redirect(url_for('index'))

    return render_template('signup.html', form = form)

