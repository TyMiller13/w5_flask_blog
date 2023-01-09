from flask import Flask

app = Flask(__name__)

#import all of the routes from the routes file into the current folder
from . import routes