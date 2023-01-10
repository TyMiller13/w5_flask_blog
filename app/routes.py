from app import app
from flask import render_template

@app.route('/')
def index():
    fruits = ['apple', 'banana', 'kiwi', 'strawberry', 'watermelon', 'pineapple']
    return render_template('index.html', name='Tyler', fruits=fruits)
    
@app.route('/posts')
def posts():
    return 'these are the post'

@app.route('/signup')
def signup():
    return render_template('signup.html')