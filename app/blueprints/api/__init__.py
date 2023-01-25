from flask import Blueprint;
# from flask_cors import CORS

api = Blueprint('api', __name__, url_prefix='/api')
# CORS(app)

from . import routes