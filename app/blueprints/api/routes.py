from flask import request
from . import api;
from app.models import Post, User

@api.route('/')
def index():
    return 'Hello this is the API'

# Endpoint to get all the posts
@api.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return [p.to_dict() for p in posts]

# Endpoint to get a single post
@api.route('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return post.to_dict()

# Endpoint to create a new post
@api.route('/posts', methods=['POST'])
def create_post():
    #check to see that the request sent a request body that is json
    if not request.is_json:
        return {'error': 'Your request content-type must be application/json'}, 400
    # Get the data from the request body
    data = request.json
    # Validate the incoming data
    for field in ['email', 'body', 'user_id']:
        #If the field is not in the request body; throw an error saying they are missing that field
        if field not in data:
            return {'error': f"{field} must be in request body"}, 400

    #Pull the fields from the request data
    email = data.get('email')
    body = data.get('body')
    user_id = data.get('user_id')

    #Create new post instance with data from request
    new_post = Post(email=email, body=body, user_id=user_id)
    #return the new post as a JSON response
    return new_post.to_dict(), 201


    #Endpoint to get existing user by id
@api.route('/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user.to_dict()
    
    
    #Endpoint to create new user
@api.route('/users', methods=["POST"])
def create_user():
    #check to see that the request sent a request body that is json
    if not request.is_json:
        return {'error': 'Your request content-type must be application/json'}, 400
    # Get the data from the request body
    data = request.json
    # Validate the incoming data
    for field in ['email', 'username', 'password']:
        #If the field is not in the request body; throw an error saying they are missing that field
        if field not in data:
            return {'error': f"{field} must be in request body"}, 400
    #Pull individual values from the request body
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    # Check to see if there are current userss withe that username /or email
    existing_user = User.query.filter((User.username == username)|(User.email == email)).all()
    if existing_user:
        return {'error': 'User with this username /or email already exists'}, 400
    #Create new User instance with data from request
    new_user = User(email=email, username=username, password=password)
    #return the new user as a JSON response
    return new_user.to_dict(), 201
    
    
